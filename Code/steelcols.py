# Program to design steel beams as per CSA S16
import math
from memberclasses import Member

### Functions

# Get basic properties of design column
def colProperties ():
    # Get length of column
    while True:
        try:
            l = float(input("Length of your column (mm): "))
            break
        except ValueError:
            print ("Please enter a valid length")

    # Get column loads
    while True:
        try:
            P = float(input("Factored axial force on column (kN): "))
            Mx = float(input("Factored moment about strong axis (kN-m): "))
            My = float(input("Factored moment about weak axis (kN-m): "))
            break
        except ValueError:
            print ("That is not a valid input, please try again")

    # Get column k value
    while True:
        try:
            k = float(input("Column k value: "))
            break
        except ValueError:
            print ("k. Take this seriously")

    # Choose section
    while True:
        type = input("What section is your column?\n1. W-Shape\n2. Angle\n3. HSS\n")
        type = type.strip()
        if type in ['1', '2', '3', '4', '5']:
            if type == '1':
                section = 'W'
            elif type == '2':
                section = 'L'
            else:
                section = 'HSS'
            break
        else:
            print ("Please choose a valid section")
    return (l, P, Mx, My, k, section)

# Choose a preliminary section for analysis
def prelimSection ( shapes ):
    st = next(i for i in (range(len(shapes))) if shapes[i][0] == desInfo[5])
    en = next(i for i in reversed(range(len(shapes))) if shapes[i][0] == desInfo[5])-1
    return st, en

def omega2 (desInfo):
    try:
        kappa = max([desInfo[2], desInfo[3]])/min([desInfo[2], desInfo[3]])
    except:
        kappa = max([desInfo[2], desInfo[3]]) # Should make code proceed as it should
    w2 = 1.75 + 1.05*kappa + 0.3*kappa**2
    if w2 > 2.5:
        w2 = 2.5
    return w2

def UCalc (case, P, column, kappa):
    if case == 1:
        w1 = 0.6 - 0.4*kappa
        if w1 < 0.4:
            w1 = 0.4
        # 13.8.4 in the code
        Cex = (math.pi**2*200000*column.Ix)/(column.length**2)
        Cey = (math.pi**2*200000*column.Iy)/(column.length**2)
        U1x = w1/(1-P/Cex)
        U1y = w1/(1-P/Cey)
    elif case == 2:
        U1x = 1
        U1y = 1

    elif case == 3:
        U1x = 1
        U1y = 1
        
    return U1x, U1y

# Iterate on prelimSection
# Need to add cases for angle and channel members
def ULS ( desInfo, shapes, column ):
    Fy = 350
    E = 200000
    G = 77000
    n = 1.34
    efficiency = 0 
    w2 = omega2(desInfo)
    try:
        kappa = max([desInfo[2], desInfo[3]])/min([desInfo[2], desInfo[3]])
    except:
        kappa = max([desInfo[2], desInfo[3]]) # Should make code proceed as it should
    beta = 0.6+0.4*(column.k*column.length/column.ry)*math.sqrt(Fy/math.pi**2/E)
    if beta > 0.85:
        beta = 0.85
    lamb = 3    
    column.CrCalc(desInfo, lamb)
    if desInfo[2] > 0 or desInfo[3] > 0:
    # Capacity check a
        column.CrCalc(desInfo, 0)
        column.MrCalc(w2)
        U1x, U1y = UCalc(1, desInfo[1], column, kappa)
        efficiency = desInfo[1]/column.Cr + (0.85*U1x*desInfo[2])/(0.9*column.Mpx)+(beta*U1y*desInfo[3])/(0.9*column.Mpy)
        # start next loop before going thru rest of calcs

        # Capacity check b 
        tempk = column.k
        column.k = 1
        column.CrCalc(desInfo, 1)
        U1x, U1y = UCalc(2, desInfo[1], column, kappa)
        efficiency = desInfo[1]/column.Cr + (0.85*U1x*desInfo[2])/(0.9*column.Mpx)+(beta*U1y*desInfo[3])/(0.9*column.Mpy)
        
        # Capacity check c
        column.k = tempk
        U1x, U1y = UCalc(3, desInfo[1], column, kappa)
        efficiency = desInfo[1]/column.Cr + (0.85*U1x*desInfo[2])/(column.Mrx)+(beta*U1y*desInfo[3])/(0.9*column.Mpy)

        # Capacity check d
        efficiency = desInfo[2]/column.Mrx + desInfo[3]/column.Mpy # Not sure if this is supposed to be Mpy
    else:
        column.CrCalc(desInfo)
        # Final check for if column passes ULS
    return column, efficiency

def SLS ( k, l, column, index ):
    klrs = [k*l/column.rx, k*l/column.ry]
    klr = max(klrs)
    
    return klr

### Main Body
shapes = []
with open('../Assets/aisc-shapes-database-v15.csv', 'r') as steelCSV:
    for row in steelCSV:
        shapes.append(row.strip().split(','))
        # Metric shape names @ column 82
        # Check excel file for referencing columns

desInfo = colProperties() # [l,P,Mx,My,k,section]
potentials = []
weights = []
st, en = prelimSection( shapes )
# Just check all members to see if they passed ULS and SLS cases
for i in range (st, en):
    column = Member ( shapes[i][:], desInfo[4], desInfo[5], desInfo[0] )

    # Check ULS Failure
    column, efficiency = ULS ( desInfo, shapes, column )
    if efficiency < 0.3 or efficiency >= 0.9:
        continue

    # Check SLS Failure
    klr = SLS ( desInfo[4], desInfo[0], column, i )
    if klr > 200:
        continue
    
    potentials.append([i, column.weight])
print(potentials)
for j in range(0, len(potentials)):
    weights.append(potentials[j][1])
index = weights.index(min(weights))

column = Member( shapes[potentials[index][0]][:], desInfo[4], desInfo[5], desInfo[0] )

print(column.name)
