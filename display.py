import time
import numpy as np
import taichi as ti
import ants as ant
import constants

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    rgb = [int(hex_code[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    rgb += [1.0]
    return rgb

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
        self.color_buffer = ti.Vector.field(n=4, dtype=ti.f32, shape=(self.height, self.width))
        self.gui = ti.ui.Window('Fourmi', res=(self.width, self.height))
        self.canvas = self.gui.get_canvas()
        self.home = home #ti.Vector(int, int)
        self.image = ti.ndarray(dtype=ti.math.vec4, shape=(self.height, self.width))
        self.pheromones_colors = ti.Vector.field(n=4, dtype=ti.f32, shape=constants.NUMBER_OF_PHEROMONES)
        self.fill_phero_colors()
        tmp = ti.tools.imread("./saved_images/dirt_bg.png")
        tmp = ti.tools.imresize(tmp, self.width, self.height)
        self.image.from_numpy(tmp)

    def fill_phero_colors(self):
        for i in range(constants.NUMBER_OF_PHEROMONES):
            self.pheromones_colors[i] = ti.Vector(hex_to_rgb(constants.colors["pheromones"][i]), dt=ti.f32)

    def init_background(self) :
        self.background = ti.Vector.field(n=4, dtype=ti.f16, shape=(self.height, self.width))

        """for i in range(self.height):
            for j in range(self.width):
                self.background[i, j] = self.image[i, j]"""


    def update_window(self, bg) :
        self.update_pixels(bg)
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
                    self.color_buffer[x, y] = ti.Vector(hex_to_rgb(constants.colors["food"]), dt=ti.f32 )
    @ti.kernel
    def generate_home_mask(self):
        home_size = int(constants.HOME_SIZE * 2 * (1/constants.HOME_ZOOM_FACTOR))
        for x in range(0, home_size):
            for y in range(0, home_size):
                distance = ti.sqrt((x - home_size)**2 + (y - home_size)**2)
                self.home_mask[x, y] = [ti.f32((150 + 2 * (home_size - distance) + 50 * ti.random()) / 255), ti.f32((75 + (home_size - distance) + 50 * ti.random())/255), 0.0, 1.0]
    @ti.kernel
    def update_home(self) :
        for x in range(-ti.static(constants.HOME_SIZE), ti.static(constants.HOME_SIZE)) :
            for y in range(-ti.static(constants.HOME_SIZE), ti.static(constants.HOME_SIZE)) :
                col = self.home_mask[(x + constants.HOME_SIZE) // constants.HOME_ZOOM_FACTOR, (y + constants.HOME_SIZE) // constants.HOME_ZOOM_FACTOR]
                self.color_buffer[ti.Vector([self.home[0] + x, self.home[1] + y])] = col
    @ti.kernel
    def update_ants(self) :
        for i in self.ants :
            self.color_buffer[int(self.ants[i])] = ti.Vector(hex_to_rgb(constants.colors["fourmis"]), dt=ti.f32)
    
    @ti.kernel            
    def update_pixels(self, bg: ti.types.ndarray(ti.math.vec4, 2)):
        for i, j in self.color_buffer:
            col = ti.Vector([0.0, 0.0, 0.0, 0.0], dt=ti.f32)
            for k in range(constants.NUMBER_OF_PHEROMONES):
                col += self.pheromones_colors[k]* ti.f32(self.grid[i, j, k])

            self.color_buffer[i, j] = col

    
    def update_grid(self, grid, ants, food, updateWindow = True) :
        self.grid = grid
        self.ants = ants
        self.food = food
        if updateWindow :
            self.update_window(self.image)


        