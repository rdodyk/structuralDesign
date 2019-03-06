import math
class Member:
    def __init__( self, properties, k, section, length ):
        self.name = properties[84]
        self.weight = float(properties[86]) * 9.81/1000
        self.area = float(properties[87])
        self.secClass = 0
        self.d = float(properties[88])
        try:
            self.bw = float(properties[114])
        except:
            pass
        try:
            self.ht = float(properties[117])
        except:
            pass
        try:
            self.b = float(properties[96])
        except:
            pass
        self.Ix = float(properties[120])*1000000
        self.Iy = float(properties[124])*1000000
        self.Zx = float(properties[121])
        self.Zy = float(properties[125])
        self.Sx = float(properties[122])
        self.Sy = float(properties[126])
        try:
            self.J = float(properties[131])*1000
        except:
            self.J = 0
        try:
            self.Cw = float(properties[132])*1000000000
        except:
            self.Cw = 0
        self.rx = float(properties[123])
        self.ry = float(properties[127])
        try:
            self.ro = float(properties[140])
        except:
            self.ro = 0
        self.Cr = 0
        self.Mpx = 0
        self.Mpy = 0
        self.Mu = 0
        self.Mrx = 0
        self.Mry = 0
        self.efficiency = 0
        self.k = k
        self.section = section
        self.length = length

    def CrCalc( self, desInfo, lamb ):
        Fy = 350
        E = 200000
        n = 1.34
        if desInfo[5] == "L":
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
            Fex = (math.pi**2*E)/(((self.k*self.length)/self.rx)**2)
            Fey = (math.pi**2*E)/(((self.k*self.length)/self.ry)**2)
            F = [Fex, Fey]
            Fe = min(F)
        if lamb != 0:
            lamb = math.sqrt(Fy/Fe)
        self.Cr = (0.9*self.area*Fy)/((1+lamb**(2*n))**(1/n))/1000

    def MrCalc( self, w2 ):
        E = 200000
        G = 77000
        Fy = 350
        self.ClassCalc()
        self.Mu = ((w2*math.pi)/self.length)*math.sqrt(E*self.Iy*G*self.J+((math.pi*E/self.length)**2)*self.Iy*self.Cw)/1000000
        if self.secClass == 1 or self.secClass == 2:
            self.Mpx = self.Zx/1000*Fy
            self.Mpy = self.Zy/1000*Fy
        else:
            self.Mpx = self.Sx/1000*Fy
            self.Mpy = self.Sy/1000*Fy

        if self.Mu > 0.67*self.Mpx:
            self.Mrx = 1.15*0.9*self.Mpx*(1-(0.28*self.Mpx/self.Mu))
            if self.Mrx > 0.9*self.Mpx:
                self.Mrx = 0.9*self.Mpx
        else:
            self.Mrx = 0.9 * self.Mu

    def ClassCalc( self ):
        class1 = 145/math.sqrt(350)
        class2 = 170/math.sqrt(350)
        class3 = 200/math.sqrt(350)
        if self.bw < class1 and self.ht < class1:
            self.secClass = 1
        elif self.bw < class2 and self.ht < class2:
            self.secClass = 2
        elif self.bw < class3 and self.ht < class3:
            self.secClass = 3
        else:
            self.secClass = 4
