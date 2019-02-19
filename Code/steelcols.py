# Program to design steel beams as per CSA S16
import math
from memberclasses import Column

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
        type = input("What section is your column?\n1. W-Shape\n2. Channel\n3. Angle\n4. Double Angle\n5. HSS\n")
        type = type.strip()
        if type in ['1', '2', '3', '4', '5']:
            if type == '1':
                section = 'W'
            elif type == '2':
                section = 'C'
            elif type == '3':
                section = 'L'
            elif type == '4':
                section = '2L'
            else:
                section = 'HSS'
            break
        else:
            print ("Please choose a valid section")
    return (l, P, Mx, My, k, section)

# Choose a preliminary section for analysis
def prelimSection ( input, shapes ):
    #E = 200000
    #Fy = 350
    #index = 0
    # Added for beam column case
    #if input[2] != 0 or input[3] != 0:
    #    P = input[1]+6*(input[2]+input[3])/2
    #else:
    #    P = input[1]

    #rInit = 100 #Just an initial guess, there's got to be a better way to do this
    #FeInit = (math.pi**2*E)/(((input[4]*input[0])/rInit)**2)
    #lb1 = (Fy/FeInit)**.5
    #A1 = (P*1000*(1+lb1**(2*1.34))**(1/1.34))/(.9*Fy)
    # Get range of members selected
    st = next(i for i in (range(len(shapes))) if shapes[i][0] == input[5])
    en = next(i for i in reversed(range(len(shapes))) if shapes[i][0] == input[5])-1

    # for i in range (st, en):
    #     if float(shapes[i][87]) < A1:
    #         index = i - 1
    #         break

    # Just use the smallest member if can't find a small enough one
    # if index == 0:
    #     index = en
    return st, en

# Iterate on prelimSection
def ULSSimple ( input, shapes, st, en, skip ):
    Fy = 350
    E = 200000
    n = 1.34
    potentials = []
    weights = []
    for i in range (st, en):
        if i in skip:
            continue

        column = Column( shapes[i][:], input[4], input[5], input[0] )
        Fex = (math.pi**2*E)/(((input[4]*input[0])/column.rx)**2)
        Fey = (math.pi**2*E)/(((input[4]*input[0])/column.ry)**2)
        F = [Fex, Fey]
        Fe = min(F)
        lamb = math.sqrt(Fy/Fe)
        column.Cr = (0.9*column.area*Fy)/((1+lamb**(2*n))**(1/n))/1000
        if column.Cr > input[1]:
            potentials.append([i,column.weight])

    for j in range(0, len(potentials)):
        weights.append(potentials[j][1])
    index = weights.index(min(weights))
    column = Column( shapes[potentials[index][0]][:], input[4], input[5], input[0] )
    return column, potentials[index][0]

def SLSSimple ( k, l, column, index, skip ):
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
st, en = prelimSection( [l, P, Mx, My, k, section], shapes )
skip = []
passed = False
while passed == False:
    column, index = ULSSimple( [l, P, Mx, My, k, section], shapes, st, en, skip )
    passed, skip = SLSSimple ( k, l, column, index, skip )

print(column.name)
