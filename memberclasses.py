class Beam:
    def __init__( self, properties ):
        self.weight = properties[84] * 9.81
        self.secClass = 0
        self.Ix = properties[118]
        self.Iy = properties[122]
        self.Zx = properties[119]
        self.Zy = properties[123]
        self.Sx = properties[120]
        self.J = properties[129]
        self.Cw = properties[130]
        self.Mp = 0
        self.Mu = 0
        self.Mr = 0

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
