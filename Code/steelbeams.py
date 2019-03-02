# Program to design steel beams as per CSA S16
import math
from memberclasses import Member

#Functions
def loadCombos(  ):
    factoredLoads = []
    loads = [0,0,0,0] #Dead, live, snow, wind

    loads[0] = input("Unfactored dead load (kN/m): ")
    loads[1] = input("Unfactored live load (kN/m): ")
    loads[2] = input("Unfactored snow load (kN/m): ")
    loads[3] = input("Unfactored wind load (kN/m): ")

    for i in range (0, len(loads)):
        if loads[i] == "":
            loads[i] = 0
        else:
            loads[i] = float(loads[i])

    for i in range (0, len(loads)):
        if i==0:
            factoredLoads.append(1.4*loads[0])
        elif i==1:
            factoredLoads.append(1.25*loads[0]+1.5*loads[1]+max([loads[2], 0.4*loads[3]]))
        elif i==2:
            factoredLoads.append(1.25*loads[0]+1.5*loads[2]+max([loads[1], 0.4*loads[3]]))
        elif i==3:
            factoredLoads.append(1.25*loads[0]+1.4*loads[3]+0.5*max([loads[1], loads[2]]))

    return (max(factoredLoads))

#All uniformly distributed loads
def shearMoment( wf, l, x, connection ):
    l = l/1000
    x = x/1000
    if connection == 1: #Simple connection
        # vMax = wf*l/2
        # mMax = (wf*l**2)/8
        if x == -0.001:
            mEq = wf*l**2/8
        else:
            vEq = wf*(l/2 - x)
            mEq = wf*x/2*(l-x)
    elif connection == 2: #Moment at both ends
        # vMax = wf*l/2
        # mMax = (wf*l**2)/12
        #mMid = (wf*length**2)/24
        if x == -0.001:
            mEq = wf*l**2/12
        else:
            vEq = wf*(l/2-x)
            mEq = wf/12*(6*l*x-l**2-6*x**2)
    elif connection == 3: #Cantilever
        # vMax = wf*l
        if x == -0.0011:
            mEq = (wf*l**2)/2
        else:
            vEq = wf*x
            mEq = wf*x**2/2
    elif connection == 4: #Simple with cantilever
        a = float(input("Cantilever Length: "))
        # vMax = (wf*(l**2-a**2))/(2*l)
        if x == -0.001:
            m1 = wf/(8*l**2)*(l+a)**2*(l-a)**2
            m2 = wf*a**2/2
            mMax = max([m1, m2])
        else:
            if x < l - a:
                vEq = wf/(2*l)*(l**2-a**2)-wf*x
                mEq = wf*x/(2*l)*(l^2-a^2-x*l)
            else:
                vEq = wf*(a-(x-(l-a)))
                mEq = wf/2*(a-(x-(l-a)))**2
    return mEq

def omega2(wf, l, connection):
    mMax = abs(shearMoment(wf, l, -1, connection))
    Ma = abs(shearMoment(wf, l, l/4, connection))
    Mb = abs(shearMoment(wf, l, l/2, connection))
    Mc = abs(shearMoment(wf, l, 3*l/4, connection))
    w2=(4*mMax)/(mMax**2+4*Ma**2+7*Mb**2+4*Mc**2)**.5
    if w2 > 2.5:
        w2 = 2.5
    return w2, [mMax, Ma, Mb, Mc]

def ULS(mDist, w2, l, beam, i, potentials):
    weights = []

    beam.MrCalc(w2)
    if beam.Mrx > mDist[0]:
        potentials.append([i, beam.weight])

    # for j in range(0, len(potentials)):
    #     weights.append(potentials[j][1])
    # index = weights.index(min(weights))
    # beam = Member( shapes[potentials[index][0]][:], 1, "W", l )
    # beam.MrCalc(w2)
    return potentials

## Start of code##
print ("Welcome to the best design program ever")

shapes = []
with open('../Assets/aisc-shapes-database-v15.csv', 'r') as steelCSV:
    for row in steelCSV:
        shapes.append(row.strip().split(','))
        # Metric shape names @ column 82
        # Check excel file for referencing columns

span = float(input("Span of your beam (mm): "))
#Tributary width of beam
while True:
    conType = int(input("How is your beam connected?\n1. Simple\n2. Moment\n3. Cantilever\n4. Simple with Cantilever\n"))
    if conType in [1, 2, 3, 4]:
        break
    else:
        print("Please choose a valid connection type.")

while True:
    t = input("Do you know the factored line load? Y/N: ")
    if t.upper() == "Y":
        wf = float(input("Input the factored load (kN/m): "))
        break
    elif t.upper() == "N":
        wf = loadCombos(  )
        break
    else:
        print("Please choose either Y or N")

st = next(i for i in (range(len(shapes))) if shapes[i][0] == "W")
en = next(i for i in reversed(range(len(shapes))) if shapes [i][0] == "W") - 1

potentials = []
w2, mDist = omega2(wf, span, conType)
for i in range (st, en):
    beam = Member(shapes[i][:], 1, "W", span) # Only designs W shapes for now
    wf = wf + 1.25*beam.weight
    potentials = ULS( mDist, w2, span, beam, i, potentials)

weights = []
for j in range(0, len(potentials)):
    weights.append(potentials[j][1])
index = weights.index(min(weights))
beam = Member( shapes[potentials[index][0]][:], 1, "W", span )
beam.MrCalc(w2)

print(beam.name)

save = input("Save this beam? ")
if save.upper() == "Y":
    fileName = input("Name of this beam: ")
    file = "../Output/{}.tex".format(fileName)
    f = open(file, "w+")
    # Begin LaTeX!
    # Outputs a .tex file with a perfectly formatted design
    output = """ \\documentclass{{article}}\n\n
                        \\usepackage{{amsmath}}\n\n
                        \\begin{{document}}
                        Factored Loads for {3}:\\\\
                        Mf: {0[0]:0.2f} kNm\\\\
                        Length: {1} mm\\\\
                        Resulted in the design of a {2.name} steel beam\\\\
                        \\textbf{{Resistance Calculation:}}\\\\
                        \\begin{{align*}}
                        \\omega_{{2}} =& \\frac{{4 M_{{max}}}}{{\\sqrt{{M_{{max}}^2 + 4M_{{a}}^2 + 7M_{{b}}^2 + 4M_{{c}}^2}}}} \\leq 2.5 && \\oint 13.6\\\\
                        \\omega_{{2}} =& \\frac{{4\\cdot{0[0]:0.2f}}}{{\\sqrt{{{0[0]:0.2f}^2 + 4\\cdot{0[1]:0.2f}^2 + 7\\cdot{0[2]:0.2f}^2 + 4\\cdot{0[3]:0.3f}^2}}}} && \\\\
                        \\omega =& {4:0.3f} && \\\\
                        M_{{u}} =& \\frac{{\\omega_{{2}}\\pi}}{{L}}\\sqrt{{EI_{{y}}GJ+(\\frac{{\\pi E}}{{L}})^2 I_{{y}}C_{{w}}}} && \\oint 13.6\\\\
                        M_{{u}} =& \\frac{{{4:0.3f}\\pi}}{{{1}}}\\sqrt{{E{2.Iy}G{2.J}+(\\frac{{\\pi E}}{{{1}}})^2 {2.Iy}\\cdot{2.Cw}}} &&\\\\
                        M_{{u}} =& {2.Mu:0.2f}&&\\\\
                        M_{{p}} =& \\phi Z F_{{y}} && \\oint 13.5\\\\
                        M_{{p}} =& 0.9\\cdot {2.Zx}\\cdot 350MPa && \\\\
                        M_{{p}} =& {2.Mp:0.2f} \\\\
                        M_{{r}} =& 1.15\\phi M_{{p}}[1-\\frac{{0.28M_{{p}}}}{{M_{{u}}}}] \\leq \\phi M_{{p}} \\textnormal{{when}} M_{{u}} > 0.67M_{{p}} && \\oint 13.6 a) i)\\\\
                        M_{{r}} =& \\phi M_{{u}} \\textnormal{{when}} M_{{u}} \\leq 0.67M_{{p}} && \\oint 13.6 a) ii)\\\\
                        M_{{r}} =& {2.Mrx:0.2f} kN\\cdot m && \\\\
                        \\end{{align*}}
                        \\end{{document}}""".format(mDist, span, beam, fileName, w2)
    f.write(output)
    f.close()
else:
    pass
