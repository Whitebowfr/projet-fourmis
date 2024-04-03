import numpy as np

class Environment():


    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))
        self.fourmis = np.array([])

    
    def addFourmi(self, fourmi):
        self.fourmis.append(fourmi)
        self.grid[fourmi.x][fourmi.y] = fourmi


env = Environment(4, 2)
print(env.grid)