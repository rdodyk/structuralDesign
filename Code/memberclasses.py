class Beam:
    def __init__( self, properties ):
        self.weight = float(properties[86]) * 9.81
        self.secClass = 0
        self.Ix = float(properties[120])
        self.Iy = float(properties[124])
        self.Zx = float(properties[121])
        self.Zy = float(properties[125])
        self.Sx = float(properties[122])
        self.J = float(properties[131])
        self.Cw = float(properties[132])
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
