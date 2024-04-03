import numpy as np

class Environment():


    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))
        self.fourmis = []

    
    def addFourmi(self, fourmi):
        self.fourmis.append(fourmi)
        self.grid[fourmi.x][fourmi.y] = fourmi

    def step(self):           
        print("step")
        self.step()
        


env = Environment(4, 2)

print(env.grid)