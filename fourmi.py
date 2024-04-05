import math
from Vectors import Vect2D
import random

SENSOR_OFFSET_DISTANCE = 2
SENSOR_SIZE = 3
SENSOR_ANGLE_DEGREES = 45
TURN_SPEED = 15
MOVE_SPEED = 15

class fourmi:

    def __init__(self, pos: Vect2D):
        self.position = pos
        self.angle = 0

    def getSensorValue(self, environnement, sensorAngleOffset) :
        sensorAngle = self.angle + sensorAngleOffset
        sensorDir = Vect2D(math.cos(sensorAngle), math.sin(sensorAngle))
        sensorPos = self.position + sensorDir * SENSOR_OFFSET_DISTANCE
        
        value = 0

        for offsetX in range(-SENSOR_SIZE, SENSOR_SIZE):
            for offsetY in range(-SENSOR_SIZE, SENSOR_SIZE):
                gridX = int(sensorPos.x + offsetX)
                gridY = int(sensorPos.y + offsetY)
                
                if gridX >= 0 and gridX < environnement.width and gridY >= 0 and gridY < environnement.height:
                    value += environnement.grid[gridX][gridY]
        
        return value
    
    def update(self, environnement, deltaT):
        forward_value = self.getSensorValue(environnement, 0)
        left_value = self.getSensorValue(environnement, SENSOR_ANGLE_DEGREES)
        right_value = self.getSensorValue(environnement, -SENSOR_ANGLE_DEGREES)

        randomSteering = random.random()

        if forward_value > left_value and forward_value > right_value :
            self.angle += 0
        elif forward_value < left_value and forward_value < right_value :
            self.angle += (randomSteering - 0.5) * 2 * TURN_SPEED * deltaT
        elif left_value > right_value :
            self.angle += randomSteering * TURN_SPEED * deltaT
        elif right_value > left_value :
            self.angle -= randomSteering * TURN_SPEED * deltaT

        direction = Vect2D(math.cos(self.angle), math.sin(self.angle))
        newPos = self.position + direction * deltaT * MOVE_SPEED

        if newPos.x < 0 or newPos.x >= environnement.width or newPos.y < 0 or newPos.y >= environnement.height :
            self.angle = random.randint(0, 360)
            newPos.x = min(environnement.width, max(0, newPos.x))
            newPos.y = min(environnement.height, max(0, newPos.y))
        else :
            previousTrail = environnement.grid[int(self.position.x)][int(self.position.y)]
            environnement.grid[int(self.position.x)][int(self.position.y)] = max(1, previousTrail)
        self.position = newPos
        

        