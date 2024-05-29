import taichi as ti
import constants
from PIL import Image
import numpy as np

ti.init(arch=ti.vulkan)

@ti.data_oriented
class Environment():    
    def __init__(self, width, height, prebuilt_path=None):
        self.width = width - 1
        self.height = height - 1
        self.path = prebuilt_path
        self.grid = ti.field(dtype=ti.f16, shape=(self.height, self.width, constants.NUMBER_OF_PHEROMONES))
        self.grid_blurred = ti.field(dtype=ti.f16, shape=(self.height, self.width, constants.NUMBER_OF_PHEROMONES))
        self.food = ti.field(dtype=ti.f32, shape=(self.height, self.width))
        self.home = ti.Vector([int(height//2), int(width//2)])
        if self.path is None:
            self.init_food()
        else:
            self.load_prebuilt()

    @ti.kernel
    def init_food(self):
        for i in range(constants.FOOD_COUNT):
            center = ti.Vector((ti.random() * self.height, ti.random() * self.width))
            while ti.sqrt((self.home[0] - center[0])**2 + (self.home[1] - center[1])**2) < constants.FOOD_SIZE + constants.HOME_SIZE:
                center = ti.Vector((ti.random() * self.height, ti.random() * self.width))
            for x in range(-ti.static(constants.FOOD_SIZE), ti.static(constants.FOOD_SIZE)):
                for y in range(-ti.static(constants.FOOD_SIZE), ti.static(constants.FOOD_SIZE)):
                    if center[0] + x >= 0 and center[0] + x < self.height and center[1] + y >= 0 and center[1] + y < self.width:
                        distance = ti.sqrt(x**2 + y**2)
                        if distance < constants.FOOD_SIZE:
                            self.food[int(center[0] + x), int(center[1] + y)] = ti.f32(1.0)
    def load_prebuilt(self):
        self.image = ti.tools.imread(self.path)
        self.image = ti.tools.imresize(self.image, self.width, self.height)
        for i in range(self.height):
            for j in range(self.width):
                if not np.array_equal(self.image[i, j], np.array([0, 0, 0])):
                    self.food[i, j] = 1.0
    @ti.kernel
    def decay(self, deltaT: ti.f16):
        for (i, j, k) in self.grid:
            self.grid[i, j, k] *= ti.f16(1 - ti.static(constants.DECAY_RATE) * deltaT)

    def __str__(self):
        return str(self.grid)
    
    @ti.kernel
    def box_blur(self):
        for i, j, k in self.grid:
            blurred_value = ti.f16(0.0)
            count = 0
            for dx in ti.static(range(-1, 2)):
                for dy in ti.static(range(-1, 2)):
                    if i + dx >= 0 and i + dx < self.height and j + dy >= 0 and j + dy < self.width:
                        blurred_value += self.grid[i + dx, j + dy, k]
                        count += 1
            self.grid_blurred[i, j, k] = ti.f16(blurred_value / count)
        for i, j, k in self.grid:
            self.grid[i, j, k] = self.grid_blurred[i, j, k]

if __name__ == "__main__":
    pass