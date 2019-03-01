import math
class Member:
    def __init__( self, properties, k, section, length ):
        self.name = properties[84]
        self.weight = float(properties[86]) * 9.81/1000
        self.area = float(properties[87])
        self.secClass = 0
        self.d = float(properties[88])
        try:
            self.b = float(properties[96])
        except:
            pass
        self.Ix = float(properties[120])
        self.Iy = float(properties[124])
        self.Zx = float(properties[121])
        self.Zy = float(properties[125])
        self.Sx = float(properties[122])
        try:
            self.J = float(properties[131])
        except:
            self.J = 0
        try:
            self.Cw = float(properties[132])
        except:
            self.Cw = 0
        self.rx = float(properties[123])
        self.ry = float(properties[127])
        try:
            self.ro = float(properties[140])
        except:
            self.ro = 0
        self.Cr = 0
        self.Mp = 0
        self.Mu = 0
        self.Mrx = 0
        self.Mry = 0
        self.efficiency = 0
        self.k = k
        self.section = section
        self.length = length

    def findClass( self ):
        Fy = 200000
        #if self.section = "W":
        if properties[114] < 7.81 & properties[117] < 59.2:
            self.secClass = 1
            self.Mp = 0.9*Fy*properties[119]
        elif properties[114] < 9.15 & properties[117] < 91.5:
            self.secClass = 2
            self.Mp = 0.9*Fy*properties[119]
        elif properties[114] < 10.77 & properties[117] < 102.3:
            self.secClass = 3
            self.Mp = 0.9*Fy*properties[120]
        else:
            self.secClass = 4
            self.Mp = 0.9*Fy*properties[120]
        #elif self.section = "HSS":
        #elif self.section = "L":
        #else:

    def CrCalc( self ):
        if input[5] == "L":
            if self.b/self.d < 1.7:
                if 0 <= self.length/self.rx and self.length/self.rx <= 80:
                    klr = 72 + 0.75*self.length/self.rx
                elif self.length/self.rx > 80:
                    klr = 32 + 1.25*self.length/self.rx
                    if klr > 200:
                        klr = 200
            else: # Gotta do something here
                print("Reference CSA S16-14 $13.3.3.4 for additional design, design is just wack")
            Fe = (math.pi**2*E)/(klr)**2
        else:
            Fex = (math.pi**2*E)/(((input[4]*input[0])/self.rx)**2)
            Fey = (math.pi**2*E)/(((input[4]*input[0])/self.ry)**2)
            F = [Fex, Fey]
            Fe = min(F)
        lamb = math.sqrt(Fy/Fe)
        self.Cr = (0.9*self.area*Fy)/((1+lamb**(2*n))**(1/n))/1000

    def MrCalc( self, w2 ):
        E = 200000
        G = 77000
        Fy = 350
        self.Mu = ((w2*math.pi)/self.length)*math.sqrt(E*self.Iy*G*self.J+(math.pi*E/self.length)**2*self.Iy*self.Cw)/1000000
        print(self.Mu)
        self.Mp = self.Zx/1000*Fy
        print(self.Mp)

        if self.Mu > 0.67*self.Mp:
            self.Mr = 1.15*0.9*self.Mp*(1-(0.28*self.Mp/self.Mu))
            if self.Mr > 0.9*self.Mp:
                self.Mr = 0.9*self.Mp
