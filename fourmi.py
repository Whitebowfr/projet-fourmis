import math
from Vectors import Vect2D
import random
import taichi as ti

SENSOR_OFFSET_DISTANCE = 2
SENSOR_SIZE = 3
SENSOR_ANGLE_RAD = 45 * 3.14 / 180
TURN_SPEED = 15
MOVE_SPEED = 15

ti.init(arch=ti.cpu)

@ti.data_oriented
class fourmi:
    def __init__(self, pos):
        self.position = pos
        self.angle = (random.random() - 0.5) * 2.0 * 3.14 / 180.0

    @ti.func
    def getSensorValue(self, environnementGrid, sensorAngleOffset: float) :
        sensorAngle = self.angle + sensorAngleOffset
        sensorDir = ti.Vector([ti.cos(sensorAngle), ti.sin(sensorAngle)])
        sensorPos = self.position + sensorDir * SENSOR_OFFSET_DISTANCE
        
        value = 0

        for offsetX in range(-SENSOR_SIZE, SENSOR_SIZE):
            for offsetY in range(-SENSOR_SIZE, SENSOR_SIZE):
                gridX = int(sensorPos.x + offsetX)
                gridY = int(sensorPos.y + offsetY)
                
                if gridX >= 0 and gridX < environnementGrid.shape[0] and gridY >= 0 and gridY < environnementGrid.shape[1]:
                    value += environnementGrid[gridX, gridY]
        
        return value
    
    @ti.func
    def update(self, environnementGrid, deltaT: float, i: int):
        forward_value = self.getSensorValue(environnementGrid, 0)
        left_value = self.getSensorValue(environnementGrid, SENSOR_ANGLE_RAD)
        right_value = self.getSensorValue(environnementGrid, -SENSOR_ANGLE_RAD)

        randomSteering = random.random()

        if forward_value > left_value and forward_value > right_value :
            pass
        elif forward_value < left_value and forward_value < right_value :
            self.angle += (randomSteering - 0.5) * 2 * TURN_SPEED * deltaT
        elif left_value > right_value :
            self.angle += randomSteering * TURN_SPEED * deltaT
        elif right_value > left_value :
            self.angle -= randomSteering * TURN_SPEED * deltaT

        direction = Vect2D(math.cos(self.angle), math.sin(self.angle))
        newPos = self.position + direction * deltaT * MOVE_SPEED

        shape = environnementGrid.shape
        if newPos.x < 0 or newPos.x >= shape[0] or newPos.y < 0 or newPos.y >= shape[1] :
            self.angle = random.randint(0, 360)
            newPos.x = min(shape[0], max(0, newPos.x))
            newPos.y = min(shape[1], max(0, newPos.y))
        elif i%10 == 0 :
            previousTrail = environnementGrid[int(self.position.x)][int(self.position.y)]
            environnementGrid[int(self.position.x)][int(self.position.y)] = max(1, previousTrail)
        self.position = newPos
        

        