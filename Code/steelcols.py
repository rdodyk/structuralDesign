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
def prelimSection ( input, shapes ):
    st = next(i for i in (range(len(shapes))) if shapes[i][0] == input[5])
    en = next(i for i in reversed(range(len(shapes))) if shapes[i][0] == input[5])-1
    return st, en

def omega2 (input):
    kappa = max([input[2], input[3]])/min([input[2], input[3]])
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
def ULS ( input, shapes, column ):
    Fy = 350
    E = 200000
    G = 77000
    n = 1.34
    weights = []
    kappa = max([input[2], input[3]])/min([input[2], input[3]])
    beta = 0.6+0.4*(column.k*column.length/column.ry)*math.sqrt(Fy/math.pi**2/E)
    if beta > 0.85:
        beta = 0.85
        
    column.CrCalc(input)
    if input[2] > 0 or input[3] > 0:
    # Capacity check a
        column.CrCalc(input, 0)
        column.MrCalc(w2)
        U1x, U1y = UCalc(1, input[1], column, kappa)
        efficiency = input[1]/column.Cr + (0.85*U1x*input[2])/(0.9*column.Mpx)+(beta*U1y*input[3])/(0.9*column.Mpy)
        # start next loop before going thru rest of calcs
        if efficiency >= 0.9:
            raise Exception()

        # Capacity check b 
        tempk = column.k
        column.k = 1
        column.CrCalc(input, 1)
        U1x, U1y = UCalc(2, input[1], column, kappa)
        efficiency = input[1]/column.Cr + (0.85*U1x*input[2])/(0.9*column.Mpx)+(beta*U1y*input[3])/(0.9*column.Mpy)
        if efficiency >= 0.9:
            raise Exception()
        
        # Capacity check c
        column.k = tempk
        U1x, U1y = UCalc(3, input[1], column, kappa)
        efficiency = input[1]/column.Cr + (0.85*U1x*input[2])/(column.Mrx)+(beta*U1y*input[3])/(0.9*column.Mpy)
        if efficiency >= 0.9:
            raise Exception()

        # Capacity check d
        efficiency = input[2]/column.Mrx + input[3]/column.Mry
        if efficiency < 0.9:
            potentials.append(column)
    else:
        column.CrCalc(input)
    # Final check for if column passes ULS
    if  efficiency < 0.9:
        potentials.append(column)


def SLS ( k, l, column, index ):
    klrs = [k*l/column.rx, k*l/column.ry]
    klr = max(klrs)

    if klr < 200:
        print("Passed SLS check!")
        return True, skip
    else:
        print("Failed SLS check :(")
        skip.append(index)
        return False, skip

### Main Body
shapes = []
with open('../Assets/aisc-shapes-database-v15.csv', 'r') as steelCSV:
    for row in steelCSV:
        shapes.append(row.strip().split(','))
        # Metric shape names @ column 82
        # Check excel file for referencing columns

[l, P, Mx, My, k, section] = colProperties()
potentials = []
st, en = prelimSection( [l, P, Mx, My, k, section], shapes )
# Just check all members to see if they passed ULS and SLS cases
for i in range (st, en):
    column = Member ( shapes, k, section, l )
    try:
        index = ULS ( [l, P, Mx, My, k, section], shapes, column )
        potentials = SLS ( k, l, column, index )
    except:
        continue

print(column.name)
