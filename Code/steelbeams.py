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
    if connection == 1: #Simple connection
        # vMax = wf*l/2
        # mMax = (wf*l**2)/8
        vEq = wf*(l/2 - x)
        mEq = wf*x/2*(l-x)
    elif connection == 2: #Moment at both ends
        # vMax = wf*l/2
        # mMax = (wf*l**2)/12
        #mMid = (wf*length**2)/24
        vEq = wf(l/2-x)
        mEq = wf/12*(6*l*x-l**2-6*x**2)
    elif connection == 3: #Cantilever
        # vMax = wf*l
        # mMax = (wf*l**2)/2
        vEq = wf*x
        mEq = wf*x**2/2
    elif connection == 4: #Simple with cantilever
        a = float(input("Cantilever Length: "))
        # vMax = (wf*(l**2-a**2))/(2*l)
        # m1 = wf/(8*l**2)*(l+a)**2*(l-a)**2
        # m2 = wf*a**2/2
        # mMax = max([m1, m2])
        if x < l - a:
            vEq = wf/(2*l)*(l**2-a**2)-wf*x
            mEq = wf*x/(2*l)*(l^2-a^2-x*l)
        else:
            vEq = wf*(a-(x-(l-a)))
            mEq = wf/2*(a-(x-(l-a)))**2

    return mEq

def omega2(wf, l, connection):
    mMax = shearMoment(wf, l, -1, connection)
    Ma = shearMoment(wf, l, l/4, connection)
    Mb = shearMoment(wf, l, l/2, connection)
    Mc = shearMoment(wf, l, 3*l/4, connection)

    w2=(4*mMax)/(mMax**2+4*Ma**2+7*Mb**2+4*Mc**2)**.5

    return w2, mMax

def ULS(mMax, w2, l, beam, i):
    potentials = []
    weights = []

    beam.MrCalc(w2)

    if beam.Mr > mMax:
        potentials.append([i, beam.weight])

    for j in range(0, len(potentials)):
        weights.append(potentials[j][1])
    index = weights.index(min(weights))
    beam = Member( shapes[potentials[index][0]][:], input[4], input[5], input[0] )
    return beam, potentials[index][0]

## Start of code##
print ("Welcome to the best design program ever")

shapes = []
with open('../Assets/aisc-shapes-database-v15.csv', 'r') as steelCSV:
    for row in steelCSV:
        shapes.append(row.strip().split(','))
        # Metric shape names @ column 82
        # Check excel file for referencing columns

span = float(input("Span of your beam: "))
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
        wf = float(input("Input the factored load: "))
        break
    elif t.upper() == "N":
        wf = loadCombos(  )
        break
    else:
        print("Please choose either Y or N")

st = next(i for i in (range(len(shapes))) if shapes[i][0] == "W")
en = next(i for i in reversed(ranged(len(shapes))) if shapes [i][0] == "W") - 1

for i in range (st, en):
    beam = Member(shapes[i][:], 1, "W", span) # Only designs W shapes for now
    wftemp = wf + 1.25*beam.weight
    w2, mMax = omega2(wftemp, l, connection)
    beam, index = ULS( mMax, w2, span, beam)
