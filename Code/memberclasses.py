import math
class Member:
    def __init__( self, properties, k, section, length ):
        self.name = properties[84]
        self.weight = float(properties[86]) * 9.81/1000
        self.area = float(properties[87])
        self.secClass = 0
        try:
            self.d = float(properties[88])
        except:
            pass
        try:
            self.tnom = float(properties[104])
        except:
            pass
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
            self.b = 100000 #Just make this really big so it fails class check?
        self.Ix = float(properties[120])*1000000
        self.Iy = float(properties[124])*1000000
        self.Zx = float(properties[121])
        self.Zy = float(properties[125])
        self.Sx = float(properties[122])
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
        self.Mp = 0
        self.Mu = 0
        self.Mrx = 0
        self.Mry = 0
        self.efficiency = 0
        self.k = k
        self.section = section
        self.length = length

    def ClassCalc( self, section ):
        if section == "W":
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
        elif section == "HSS":
            class1 = 420/math.sqrt(350)
            class2 = 525/math.sqrt(350)
            class3 = 670/math.sqrt(350)
            bt = self.b/self.tnom
            if bt < class1:
                self.secClass = 1
            elif bt < class2:
                self.secClass = 2
            elif bt < class3:
                self.secClass = 3
            else:
                self.secClass = 4
