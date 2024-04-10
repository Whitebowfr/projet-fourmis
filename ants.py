import taichi as ti

SENSOR_OFFSET_DISTANCE = 2
SENSOR_SIZE = 3
SENSOR_ANGLE_RAD = 45 * 3.14 / 180
TURN_SPEED = 30
MOVE_SPEED = 15

ti.init(arch=ti.cpu)

@ti.data_oriented
class Ants :
    def __init__(self, N, grid) :
        self.n = N
        self.positions = ti.Vector.field(2, dtype=ti.f32, shape=self.n)
        self.angles = ti.field(dtype=ti.f32, shape=self.n)
        self.grid = grid
        self.place_ants()

    @ti.kernel
    def place_ants(self):
        for i in range(self.n):
            angle = ti.random() * 2 * 3.14
            radius = ti.sqrt(ti.random()) * (self.grid.shape[0] / 2)
            x = radius * ti.cos(angle) + self.grid.shape[0] / 2
            y = radius * ti.sin(angle) + self.grid.shape[1] / 2
            self.positions[i] = ti.Vector([x, y])
            self.angles[i] = angle
    
    @ti.kernel
    def update(self, deltaT: float) :
        for i in range(self.n) :
            self.update_fourmi(i, deltaT)

    @ti.func
    def update_fourmi(self, i: int, deltaT: float):
        forward_value = self.getSensorValue(i, 0)
        left_value = self.getSensorValue(i, SENSOR_ANGLE_RAD)
        right_value = self.getSensorValue(i, -SENSOR_ANGLE_RAD)

        randomSteering = ti.random()

        if forward_value > left_value and forward_value > right_value :
            pass
        elif forward_value < left_value and forward_value < right_value :
            self.angles[i] += (randomSteering - 0.5) * 2 * TURN_SPEED * deltaT
        elif left_value > right_value :
            self.angles[i] += randomSteering * TURN_SPEED * deltaT
        elif right_value > left_value :
            self.angles[i] -= randomSteering * TURN_SPEED * deltaT

        direction = ti.Vector((ti.cos(self.angles[i]), ti.sin(self.angles[i])), dt=ti.f32)
        newPos = self.positions[i] + direction * deltaT * MOVE_SPEED

        shape = self.grid.shape
        if newPos[0] < 0 or newPos[0] >= shape[0] or newPos[1] < 0 or newPos[1] >= shape[1] :
            self.angles[i] = ti.random() * 2 * 3.14
            newPos[0] = min(shape[0], max(0, newPos[0]))
            newPos[1] = min(shape[1], max(0, newPos[1]))
        else :
            previousTrail = self.grid[int(self.positions[i][1]), int(self.positions[i][0])]
            self.grid[int(self.positions[i][1]), int(self.positions[i][0])] = max(1, previousTrail)
        self.positions[i] = newPos
    
    @ti.func
    def getSensorValue(self, i: int, sensorAngleOffset: float) :
        sensorAngle = self.angles[i] + sensorAngleOffset
        sensorDir = ti.Vector([ti.cos(sensorAngle), ti.sin(sensorAngle)])
        sensorPos = self.positions[i] + sensorDir * SENSOR_OFFSET_DISTANCE
        
        value = 0.0

        for offsetX in range(-SENSOR_SIZE, SENSOR_SIZE):
            for offsetY in range(-SENSOR_SIZE, SENSOR_SIZE):
                gridX = int(sensorPos[0] + offsetX)
                gridY = int(sensorPos[1] + offsetY)
                
                if gridX >= 0 and gridX < self.grid.shape[0] and gridY >= 0 and gridY < self.grid.shape[1]:
                    value += self.grid[gridX, gridY]
        
        return value