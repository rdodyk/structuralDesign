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
# Need to add cases for angle and channel members
def ULS ( input, shapes, column ):
    Fy = 350
    E = 200000
    G = 77000
    n = 1.34
    weights = []
    
    column.CrCalc(input)
    if column.Cr > input[1]:
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
    index = ULS ( [l, P, Mx, My, k, section], shapes, column )
    potentials = SLS ( k, l, column, index )

print(column.name)
