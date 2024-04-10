import time
import numpy as np
from fourmi import fourmi
from Vectors import Vect2D
import taichi as ti

ti.init(arch=ti.vulkan)

@ti.data_oriented
class Display() :

    def __init__(self, width, height) :
        self.width = width
        self.height = height
        self.prev_time = time.time()
        self.grid = ti.field(dtype=float, shape=(self.height, self.width))
        self.ants = []
        self.res = (self.width, self.height)
        self.color_buffer = ti.Vector.field(n=3, dtype=float, shape=(self.height, self.width))
        self.gui = ti.GUI('Fourmi', res=(self.width, self.height), fast_gui=True)
        
    def update_window(self) :
        self.update_pixels()
        self.update_ants()
        self.gui.set_image(self.color_buffer)
        self.gui.show()

    @ti.kernel
    def update_ants(self) :
        for i in self.ants :

            self.color_buffer[int(self.ants[i][1]), int(self.ants[i][0])] = ti.Vector([1,0,0])
    
    @ti.kernel            
    def update_pixels(self):
        for i, j in self.color_buffer :
            col = self.grid[i, j]
            self.color_buffer[i, j] = ti.Vector([col] * 3)
    
    def update_grid(self, grid, ants, updateWindow = True) :
        self.grid = grid
        self.ants = ants.positions
        if updateWindow :
            self.update_window()

if __name__ == '__main__' :
    app = Display(1000,1000)
    while True :
        app.update_window()
        a = np.random.randint(low=255, size=(100, 100, 3), dtype=np.uint8) # Original
        app.update_grid(a, [])
        
        