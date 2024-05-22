import taichi as ti
import constants

ti.init(arch=ti.vulkan)

@ti.data_oriented
class Environment():    
    def __init__(self, width, height):
        self.width = width - 1
        self.height = height - 1
        self.grid = ti.field(dtype=ti.f16, shape=(self.height, self.width, constants.NUMBER_OF_PHEROMONES))
        self.grid_blurred = ti.field(dtype=ti.f16, shape=(self.height, self.width, constants.NUMBER_OF_PHEROMONES))
        self.food = ti.Vector.field(2, dtype=ti.f32, shape=constants.FOOD_COUNT)
        self.home = ti.Vector([int(height//2), int(width//2)])
        self.init_food()

    @ti.kernel
    def init_food(self):
        for i in range(ti.static(self.food.shape[0])):
            self.food[i] = ti.Vector((ti.random() * self.height, ti.random() * self.width))
    
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
    env = Environment(15, 15)
    env.box_blur()
    print(env)