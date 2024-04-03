import numpy as np

class Environment():


    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.array([[0 for i in range(width)] for j in range(height)])
        self.fourmis = []

    
    def addFourmi(self, fourmi):
        self.fourmis.append(fourmi)
        self.grid[fourmi.x][fourmi.y] = fourmi
        
    def searchFourmi(self, x, y):
        for fourmi in self.fourmis:
            if fourmi.x == x and fourmi.y == y:
                return True
        return False
    
    def decay(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] > 0:
                    self.grid[y][x] -= 1

    def __str__(self):
        return str(self.grid)
    
    def pschittt(self, x, y):
        self.grid[y][x] += 200
        if self.grid[y][x] > 255:
            self.grid[y][x] = 255

    def blur(self, x, y):
        pass


    def spread(self):
        pass
        
   
        

env = Environment(15,15)
env.pschittt(10, 10)
print(env)