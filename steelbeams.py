# Program to design steel beams as per CSA S16
import math
from memberclasses import Beam

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

def shearMoment( wf, l, connection ):
    if connection == 1: #Simple connection
        vMax = wf*l/2
        mMax = (wf*l**2)/8
    elif connection == 2: #Moment
        vMax = wf*l/2
        mMax = (wf*l**2)/12
        #mMid = (wf*length**2)/24
    elif connection == 3: #Cantilever
        vMax = wf*l
        mMax = (wf*l**2)/2
    elif connection == 4: #Simple with cantilever
        a = float(input("Cantilever Length: "))
        vMax = (wf*(l**2-a**2))/(2*l)
        m1 = wf/(8*l**2)*(l+a)**2*(l-a)**2
        m2 = wf*a**2/2
        mMax = max([m1, m2])

    return (vMax, mMax)

def sizeMember(Vf, Mf, shapes, wf, l):
    Fy = 350 #MPa
    E = 200000#MPa
    G = 77000#MPa
    potentials = []
    weights = []
    index = 0
    #Preliminary Sizing
    for i in range(1, 282):
        if Mf < Fy*float(shapes [i][121])/1000*.15/10*l and Fy*float(shapes [i][121])/1000*.15/10*l < Mf*1.1: #Zx col 119
            potentials.append(i)
    print(potentials)
    for j in range (0, len(potentials)):
        weights.append(shapes[potentials[j]][86])

    if weights ==[]:
        beam = Beam( shapes[284][:]) #Just chooses ligtest W Shape
    else:
        index = weights.index(min(weights))
        beam = Beam( shapes[potentials[index]][:] )

    #Get new factored weight including self weight of member
    wf = wf + beam.weight
    (Vf, Mf) = shearMoment( wf, span, conType )

    #Where we left off
    w2=(4*Mf)/(Mf**2+4*Ma**2+7*Mb**2+4*Mc**2)**.5 #need to get moment distribution
    Mu = (w2*math.pi()/l)*(E*shapes[122][index]*G*shapes[129][index]+((math.pi()*E)/l)**2*shapes[122][index]*shapes[130][index])**.5

    if Mu > 0.67*Mp:
        Mr = 1.15*.9*Mp*(1-(0.28*Mp)/Mu)
        if Mr > Mp:
            Mr = Mp
    else:
        Mr = 0.9 * Mu

print ("Welcome to the best design program ever")

shapes = []
with open('Assets/aisc-shapes-database-v15.csv', 'r') as steelCSV:
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

(V, M) = shearMoment( wf, span, conType)
sizeMember(V, M, shapes, wf, span)
