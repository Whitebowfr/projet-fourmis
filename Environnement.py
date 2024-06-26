import numpy as np
DECAY_RATE = 0.1

class Environment():

    def __init__(self, width, height):
        self.width = width - 1
        self.height = height - 1
        self.grid = np.array([[0.0 for _ in range(width)] for _ in range(height)])
        self.fourmis = []


    def addFourmi(self, fourmi):
        self.fourmis.append(fourmi)
    
    def decay(self, deltaT):
        self.grid -= DECAY_RATE * deltaT
        self.grid = np.maximum(self.grid, 0)

    def __str__(self):
        return str(self.grid)
    
    def add_pheromone(self, x, y, type = None):
        self.grid[y][x] += 200
        if self.grid[y][x] > 255:
            self.grid[y][x] = 255

    def spread_here(self, x, y):
        value = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+i >= 0 and x+i < self.width and y+j >= 0 and y+j < self.height:
                    value += self.grid[y+j][x+i]
        return int(value / 9)


    def spread(self):
        grid_copy = []
        for y in range(len(self.grid)):
            grid_copy.append([])
            for x in range(len(self.grid[y])):
                grid_copy[y].append(self.spread_here(x, y))
        self.grid = grid_copy
        
    def affichage_debugging(self):
        print("_" *3* len(self.grid[0]))
        for y in range(len(self.grid)):
            print("[", end="")
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != 0:
                    print(self.grid[y][x], end=",")
                else:
                    print("  ", end=",")
            print("]\n")

        print()
        
if __name__ == "__main__":
    env = Environment(15,15)
    env.pschittt(10, 10)
    env.spread()
    env.affichage_debugging()
    env.spread()
    env.affichage_debugging()