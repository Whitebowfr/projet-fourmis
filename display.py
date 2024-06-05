import time
import numpy as np
import taichi as ti
import ants as ant
import constants

@ti.data_oriented
class Display() :

    def __init__(self, width, height, home) :
        self.width = ti.static(width)
        self.height = ti.static(height)
        self.prev_time = time.time()
        self.grid = ti.field(dtype=float, shape=(self.height, self.width, constants.NUMBER_OF_PHEROMONES))
        self.ants = []
        self.food = []
        self.home_mask = ti.Vector.field(n=4, dtype=ti.f16, shape=(2 * constants.HOME_SIZE, 2 * constants.HOME_SIZE))
        self.generate_home_mask()
        self.res = (self.width, self.height)
        self.color_buffer = ti.Vector.field(n=4, dtype=ti.u8, shape=(self.height, self.width))
        self.gui = ti.ui.Window('Fourmi', res=(self.width, self.height))
        self.canvas = self.gui.get_canvas()
        self.home = home #ti.Vector(int, int)


        
    def update_window(self) :
        self.update_pixels()
        self.update_ants()
        if not ti.static(constants.HIDE_MARKERS) :
            self.update_food()
            self.update_home()
        self.canvas.set_image(self.color_buffer)
        self.gui.show()

    @ti.kernel
    def update_food(self):
        for x in range(self.food.shape[0]):
            for y in range(self.food.shape[1]):
                if self.food[x, y] != 0 :
                    self.color_buffer[x, y] = ti.Vector([0, 255, 0, 255], dt=ti.u8 )
    @ti.kernel
    def generate_home_mask(self):
        home_size = int(constants.HOME_SIZE * 2 * 0.125)
        for x in range(0, home_size):
            for y in range(0, home_size):
                distance = ti.sqrt((x - home_size)**2 + (y - home_size)**2)
                self.home_mask[x, y] = [150 + 2 * (home_size - distance) + 50 * ti.random(), 75 + (home_size - distance) + 50 * ti.random(), 0, 255]
    @ti.kernel
    def update_home(self) :
        for x in range(-ti.static(constants.HOME_SIZE), ti.static(constants.HOME_SIZE)) :
            for y in range(-ti.static(constants.HOME_SIZE), ti.static(constants.HOME_SIZE)) :
                col = self.home_mask[int(0.125 * (x + constants.HOME_SIZE - 4)), int(0.125 * (y + constants.HOME_SIZE - 4))]
                self.color_buffer[ti.Vector([self.home[0] + x, self.home[1] + y])] = col
    @ti.kernel
    def update_ants(self) :
        for i in self.ants :
            self.color_buffer[int(self.ants[i])] = ti.Vector([255,0,0, 255], dt=ti.u8)
    
    @ti.kernel            
    def update_pixels(self):
        for i, j in self.color_buffer:
            col = ti.Vector([0, 0, 0, 0], dt=ti.u8)
            for k in range(constants.NUMBER_OF_PHEROMONES):
                if k != 0 :
                    col += ti.Vector([0, 0,ti.u8(self.grid[i, j, k] * 255), 0], dt=ti.u8)
                else :
                    col = ti.Vector([ti.u8(self.grid[i, j, k] * 255)] * 2 + [0,0], dt=ti.u8)

            self.color_buffer[i, j] = col

    
    def update_grid(self, grid, ants, food, updateWindow = True) :
        self.grid = grid
        self.ants = ants
        self.food = food
        if updateWindow :
            self.update_window()

if __name__ == '__main__' :
    ti.init(arch=ti.vulkan)
    app = Display(1000,1000)
    while True :
        app.update_window()
        a = np.random.randint(low=255, size=(100, 100, 3), dtype=np.uint8) # Original
        app.update_grid(a, [])
        
        