import numpy as np
import taichi as ti
DECAY_RATE = 0.5
SPREAD_RATE = 3

ti.init(arch=ti.vulkan)

@ti.data_oriented
class Environment():
    def __init__(self, width, height):
        self.width = width - 1
        self.height = height - 1
        self.grid = ti.field(dtype=float, shape=(self.height, self.width))
        self.grid_blurred = ti.field(dtype=float, shape=(self.height, self.width))
    
    @ti.kernel
    def decay(self, deltaT: float):
        for (i, j) in self.grid:
            self.grid[i, j] *= 1 - DECAY_RATE * deltaT

    def __str__(self):
        return str(self.grid)
    
    def pschittt(self, x, y):
        self.grid[y][x] += 200
        if self.grid[y][x] > 255:
            self.grid[y][x] = 255
    
    @ti.kernel
    def box_blur(self, deltaT: float):
        for i, j in self.grid:
            blurred_value = 0.0
            count = 0
            for dx in ti.static(range(-1, 2)):
                for dy in ti.static(range(-1, 2)):
                    if i + dx >= 0 and i + dx < self.height and j + dy >= 0 and j + dy < self.width:
                        blurred_value += self.grid[i + dx, j + dy]
                        count += 1
            self.grid_blurred[i, j] = blurred_value / count
        for i, j in self.grid:
            self.grid[i, j] = self.grid_blurred[i, j]

if __name__ == "__main__":
    env = Environment(15, 15)
    env.pschittt(10, 10)
    env.box_blur()
    print(env)

    

    """@ti.func
    def spread_here(self, x: int, y: int):
        value = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+i >= 0 and x+i < self.width and y+j >= 0 and y+j < self.height:
                    value += self.grid[y+j, x+i]
        return value / 9

    @ti.kernel
    def spread(self, deltaT: float):
        for x, y in self.grid :
            self.grid_blurred[y, x] = self.spread_here(x, y)
        for x,y in self.grid_blurred :
            self.grid[y, x] = self.grid_blurred[y, x]"""