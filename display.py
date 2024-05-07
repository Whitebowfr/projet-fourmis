import time
import numpy as np
import taichi as ti
import ants as ant
import constants

ti.init(arch=ti.gpu)

@ti.data_oriented
class Display() :

    def __init__(self, width, height, home) :
        self.width = ti.static(width)
        self.height = ti.static(height)
        self.prev_time = time.time()
        self.grid = ti.field(dtype=float, shape=(self.height, self.width, constants.NUMBER_OF_PHEROMONES))
        self.ants = []
        self.food = []
        self.res = (self.width, self.height)
        self.color_buffer = ti.Vector.field(n=3, dtype=float, shape=(self.height, self.width))
        self.gui = ti.GUI('Fourmi', res=(self.width, self.height), fast_gui=True)
        self.home = home
        
    def update_window(self) :
        self.update_pixels()
        #self.update_ants()
        if not ti.static(constants.HIDE_MARKERS) :
            self.update_food()
            self.update_home()
        self.gui.set_image(self.color_buffer)
        self.gui.show()

    @ti.kernel
    def update_food(self) :
        for i in range(self.food.shape[0]):
            for x in range(-constants.FOOD_SIZE, constants.FOOD_SIZE) :
                for y in range(-constants.FOOD_SIZE, constants.FOOD_SIZE) :
                    self.color_buffer[int(self.food[i] + ti.Vector([x, y]))] = ti.Vector([0, 1, 0])

    @ti.kernel
    def update_home(self) :
        for x in range(-constants.HOME_SIZE, constants.HOME_SIZE) :
            for y in range(-constants.HOME_SIZE, constants.HOME_SIZE) :
                self.color_buffer[self.home + ti.Vector([y, x])] = ti.Vector([0, 0, 1])
    @ti.kernel
    def update_ants(self) :
        for i in self.ants :
            self.color_buffer[int(self.ants[i])] = ti.Vector([1,0,0])
    
    @ti.kernel            
    def update_pixels(self):
        for i, j in self.color_buffer :
            col = ti.Vector([0.0] * 3)
            for k in range(self.grid.shape[2]) :
                if k == 1 :
                    col += ti.Vector([0.0, self.grid[i, j, k], 0.0])
                else :
                    col += ti.Vector([self.grid[i, j, k] / 2] * 3)
            self.color_buffer[i, j] = col
    
    def update_grid(self, grid, ants, food, updateWindow = True) :
        self.grid = grid
        self.ants = ants
        self.food = food
        if updateWindow :
            self.update_window()

if __name__ == '__main__' :
    app = Display(1000,1000)
    while True :
        app.update_window()
        a = np.random.randint(low=255, size=(100, 100, 3), dtype=np.uint8) # Original
        app.update_grid(a, [])
        
        