import taichi as ti
import constants

ti.init(arch=ti.vulkan)

@ti.data_oriented
class Ants :
    def __init__(self, N, grid, home, foodgrid, number_of_pheromones = 1) :
        self.n = ti.static(N)
        self.positions = ti.Vector.field(2, dtype=ti.f32, shape=self.n)
        self.angles = ti.field(dtype=ti.f32, shape=self.n)
        self.grid = grid
        self.foodgrid = foodgrid
        self.home = home
        self.number_of_pheromones = number_of_pheromones
        self.has_food = ti.field(dtype=bool, shape=self.n)
        self.place_ants_home()

    @ti.kernel
    def place_ants_random(self):
        for i in range(self.n):
            angle = ti.f32(ti.random() * 2 * 3.14)
            radius = ti.sqrt(ti.random()) * (self.grid.shape[0] / 2)
            x = ti.f32(radius * ti.cos(angle) + self.grid.shape[0] / 2)
            y = ti.f32(radius * ti.sin(angle) + self.grid.shape[1] / 2)
            self.positions[i] = ti.Vector([x, y])
            self.angles[i] = angle

    @ti.kernel
    def place_ants_home(self) :
        for i in range(self.n) :
            angle = ti.random() * 2 * 3.14
            self.positions[i] = self.home
            self.angles[i] = ti.f32(angle)
    
    @ti.kernel
    def update(self, deltaT: ti.f32) :
        for i in range(ti.static(self.n)) :
            self.update_fourmi(i, deltaT)

    @ti.func
    def update_fourmi(self, i: int, deltaT: ti.f32):
        pheromone = 0
        phb = 0
        if ti.static(self.number_of_pheromones) > 1 :
            pheromone = 1 if self.has_food[i] else 0
            phb = abs(pheromone - 1)
        
        forward_value = self.getSensorValue(i, 0, phb)
        left_value = self.getSensorValue(i, ti.static(constants.SENSOR_ANGLE_RAD), phb)
        right_value = self.getSensorValue(i, -ti.static(constants.SENSOR_ANGLE_RAD), phb)

        randomSteering = ti.random() * ti.static(constants.RANDOM_FACT)

        if forward_value > left_value and forward_value > right_value :
            pass
        elif forward_value < left_value and forward_value < right_value :
            self.angles[i] += (randomSteering - 0.5) * 2 * ti.static(constants.TURN_SPEED) * deltaT
        elif left_value > right_value :
            self.angles[i] += randomSteering * ti.static(constants.TURN_SPEED) * deltaT
        elif right_value > left_value :
            self.angles[i] -= randomSteering * ti.static(constants.TURN_SPEED) * deltaT

        direction = ti.Vector((ti.cos(self.angles[i]), ti.sin(self.angles[i])), dt=ti.f32)
        newPos = self.positions[i] + direction * deltaT * ti.static(constants.MOVE_SPEED)

        shape = self.grid.shape
        if newPos[0] < 0 or newPos[0] >= shape[0] or newPos[1] < 0 or newPos[1] >= shape[1] :
            self.angles[i] = ti.f32(ti.random() * 2 * 3.14)
            newPos[0] = min(shape[0], max(0, newPos[0]))
            newPos[1] = min(shape[1], max(0, newPos[1]))
        else :
            previousTrail = self.grid[int(self.positions[i]), pheromone]
            self.grid[int(self.positions[i]), pheromone] = max(1, previousTrail)

        if ti.static(self.number_of_pheromones) > 1 :
            if self.isInRectangle(self.positions[i], self.home, ti.static(constants.HOME_SIZE)) and self.has_food[i] :
                self.has_food[i] = False
                self.angles[i] -= ti.f32(3.14)
            if not self.has_food[i] :
                for f in range(self.foodgrid.shape[0]) :
                    if self.isInRectangle(self.positions[i], self.foodgrid[f], ti.static(constants.FOOD_SIZE)) :
                        self.has_food[i] = True
                        self.angles[i] -= ti.f32(3.14)
        self.positions[i] = newPos

    @ti.func
    def isEqual(self, vec1: ti.template(), vec2: ti.template()) -> bool : # type: ignore
        return int(vec1[0]) == int(vec2[0]) and int(vec1[1]) == int(vec2[1])
    
    @ti.func
    def isInRectangle(self, point: ti.template(), rectangle_center: ti.template(), rectangle_radius: int) -> bool : # type: ignore
            x = point[0]
            y = point[1]
            rect_x = rectangle_center[0]
            rect_y = rectangle_center[1]
            
            return x > rect_x - rectangle_radius and x < rect_x + rectangle_radius and y > rect_y - rectangle_radius and y < rect_y + rectangle_radius

    
    @ti.func
    def getSensorValue(self, i: int, sensorAngleOffset: float, pheromone: int) -> int :
        sensorAngle = self.angles[i] + sensorAngleOffset
        sensorDir = ti.Vector([ti.cos(sensorAngle), ti.sin(sensorAngle)])
        sensorPos = self.positions[i] + sensorDir * ti.static(constants.SENSOR_OFFSET_DISTANCE)
        
        value = 0.0

        for offsetX in range(-ti.static(constants.SENSOR_SIZE), ti.static(constants.SENSOR_SIZE)):
            for offsetY in range(-ti.static(constants.SENSOR_SIZE), ti.static(constants.SENSOR_SIZE)):
                gridX = int(sensorPos[0] + offsetX)
                gridY = int(sensorPos[1] + offsetY)
                
                if gridX >= 0 and gridX < self.grid.shape[0] and gridY >= 0 and gridY < self.grid.shape[1]:
                    if ti.static(self.number_of_pheromones) > 1 :
                        if self.has_food[i] :
                            if self.isInRectangle(ti.Vector([gridX, gridY]), self.home, ti.static(constants.HOME_SIZE)) :
                                value += 1
                        else :
                            for k in range(self.foodgrid.shape[0]) :
                                if self.isInRectangle(ti.Vector([gridX, gridY]), self.foodgrid[k], ti.static(constants.FOOD_SIZE)) :
                                    value += 1
                    value += self.grid[gridX, gridY, pheromone]
        
        return value