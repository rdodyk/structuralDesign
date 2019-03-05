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
def ULSSimple ( input, shapes, st, en, skip ):
    Fy = 350
    E = 200000
    G = 77000
    n = 1.34
    potentials = []
    weights = []
    for i in range (st, en):
        if i in skip:
            continue

        column = Member( shapes[i][:], input[4], input[5], input[0] )
        # Double angle case, but don't feel like making it work really
        # if input[5] == "2L":
        #     omega = 1-((column.ro**2-column.rx**2-column.ry**2)/(column.ro**2))
        #     Fex = (math.pi**2*E)/((column.k*column.length/column.rx)**2) # Add kx and ky, kz is always 1 tho
        #     Fey = (math.pi**2*E)/((column.k*column.length/column.ry)**2) #Add Lx and Ly to column properties
        #     Fez = ((math.pi**2*E*column.Cw)/((column.k*column.length)**2)+G*column.J)*(1/(column.area*column.ro**2))
        #     #Need to calculate Feyz as per code
        #     Feyz = (Fey+Fez)/(2*omega)*(1-math.sqrt(1-((4*Fey*Fez*omega)/(Fey+Fez)**2)))
        #     Fe = min([Fex, Feyz])
        if input[5] == "L":
            if column.b/column.d < 1.7:
                if 0 <= column.length/column.rx and column.length/column.rx <= 80:
                    klr = 72 + 0.75*column.length/column.rx
                elif column.length/column.rx > 80:
                    klr = 32 + 1.25*column.length/column.rx
                    if klr > 200:
                        klr = 200
                else:
                    continue
            else:
                print("Reference CSA S16-14 $13.3.3.4 for additional design, design is just wack")
                continue
            Fe = (math.pi**2*E)/(klr)**2

        else:
            Fex = (math.pi**2*E)/(((input[4]*input[0])/column.rx)**2)
            Fey = (math.pi**2*E)/(((input[4]*input[0])/column.ry)**2)
            F = [Fex, Fey]
            column.Fe = min(F)

        column.lamb = math.sqrt(Fy/column.Fe)
        column.Cr = (0.9*column.area*Fy)/((1+column.lamb**(2*n))**(1/n))/1000
        if column.Cr > input[1]:
            potentials.append([i,column.weight])

    for j in range(0, len(potentials)):
        weights.append(potentials[j][1])
    index = weights.index(min(weights))
    #This is ugly, could fix with method in member class
    column = Member( shapes[potentials[index][0]][:], input[4], input[5], input[0] )
    #Something goes wrong here
    column.Fe = (math.pi**2*E)/(((input[4]*input[0])/column.ry)**2)
    column.lamb = math.sqrt(Fy/column.Fe)
    column.Cr = (0.9*column.area*Fy)/((1+column.lamb**(2*n))**(1/n))/1000
    return column, potentials[index][0]

def SLSSimple ( k, l, column, index, skip ):
    column.ClassCalc()
    if column.secClass != 1:
        skip.append(index)
        return False, skip
    else:
        return True, skip

# Designs beam columns, but only with point moments at the top of the column
def ULSHard ( input, shapes, st, en, skip ):
    Fy = 350
    E = 200000
    G = 77000
    n = 1.34
    potentials = []
    eff = []
    weights = []
    for i in range (st, en):
        if i in skip:
            continue
        for i in (1, 3):
            #Find compressive resistance
            column, index = ULSSimple ( input, shapes, st, en, skip )
            #Find moment resistance
            print("Find moment resistance here")

            #Find column efficiency
            column.efficiency = input[1]/column.Cr + (0.85*U1x*input[2])/column.Mrx + (B*U1y*input[3])/column.Mry
            #Test to see if column meets criteria
            eff.append(column.efficiency)
        if max(eff) <= .85 and max(eff) > .6:
            potentials.append([i,column.weight])

    for j in range(0, len(potentials)):
        weights.append(potentials[j][1])
    index = weights.index(min(weights))
    column = Column( shapes[potentials[index][0]][:], input[4], input[5], input[0] )
    return column, potentials[index][0]

def SLSHard ( column, index, skip ):
    print ("Hi")

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
if Mx == 0 and My == 0:

    while passed == False:
        column, index = ULSSimple ( [l, P, Mx, My, k, section], shapes, st, en, skip )
        passed, skip = SLSSimple ( k, l, column, index, skip )

else:
    while passed == False:
        column, index = ULSHard ( [l, P, Mx, My, k, section], shapes, st, en, skip )
        passed, skip = SLSHard ( column, index, skip )

print(column.name)

save = input("Save this column? ")
if save.upper() == "Y":
    fileName = input("Name of this Column: ")
    file = "../Output/{}.tex".format(fileName)
    f = open(file, "w+")
    # Begin LaTeX!
    # Outputs a .tex file with a perfectly formatted design
    output = """ \\documentclass{{article}}\n\n
                        \\usepackage{{amsmath}}\n\n
                        \\begin{{document}}
                        Factored Loads for {6}:\\\\
                        Axial Compression: {0} kN, Mx: {1} kN$\\cdot$m, My: {2} kN$\\cdot$m\\\\
                        Length: {3} mm, k: {4}\\\\
                        Resulted in the design of a {5.name} class {5.secClass} steel column\\\\
                        \\textbf{{Resistance Calculation:}}\\\\
                        \\begin{{align*}}
                        F_{{e}} =& \\frac{{\\pi^2 E}}{{(\\frac{{kl}}{{r}})^2}} && \\oint 13.3.1\\\\
                        F_{{ex}} =& \\frac{{\\pi^2 E}}{{(\\frac{{{4} \\cdot {3} mm}}{{{5.rx:0.2f} mm}})^2}} && \\\\
                        F_{{ey}} =& \\frac{{\\pi^2 E}}{{(\\frac{{{4} \\cdot {3} mm}}{{{5.ry:0.2f} mm}})^2}} && \\\\
                        F_{{e}} =& min \\begin{{cases}}
                        F_{{ex}}\\\\
                        F_{{ey}}\\\\
                        \\end{{cases}} = {5.Fe:0.2f} MPa && \\oint 13.3.1\\\\
                        \\lambda =& \\sqrt{{\\frac{{F_{{y}}}}{{F_{{e}}}}}} && \\oint 13.3.1\\\\
                        \\lambda =& \\sqrt{{\\frac{{350 MPa}}{{{5.Fe:0.2f} MPa}}}} = {5.lamb:0.2f} &&\\\\
                        C_{{r}} =& \\frac{{\\phi A F_{{y}}}}{{(1+\\lambda^{{2n}})^\\frac{{1}}{{n}}}} && \\oint 13.3.1\\\\
                        C_{{r}} =& \\frac{{0.9 \\cdot {5.area} mm \\cdot 350 MPa}}{{(1+{5.lamb:0.2f}^{{2 \\cdot 1.34}})^\\frac{{1}}{{1.34}}}} &&\\\\
                        C_{{r}} =& {5.Cr:0.0f} kN
                        \\end{{align*}}
                        \\end{{document}}""".format(P, Mx, My, l, k, column, fileName)
    f.write(output)
    f.close()
else:
    pass
