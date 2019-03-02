import math
class Member:
    def __init__( self, properties, k, section, length ):
        self.name = properties[84]
        self.weight = float(properties[86]) * 9.81
        self.area = float(properties[87])
        self.secClass = 0
        try:
            self.d = float(properties[88])
        except:
            self.d = 0
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
        self.Fe = 0
        self.lamb = 0
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
