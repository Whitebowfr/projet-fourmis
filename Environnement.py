class Environnent():

    #__slots__

    def __init__(self, size):
        self.size = size
        self.grid = [[0 for i in range(size)] for j in range(size)]
        self.fourmis = []

    
    def addFourmi(self, fourmi):
        self.fourmis.append(fourmi)
        self.grid[fourmi.x][fourmi.y] = fourmi