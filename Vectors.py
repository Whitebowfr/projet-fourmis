import math
import random

class Vect2D:
    def __init__(self, x=0, y=0, randomPos=False):
        if randomPos :
            self.x = random.randint(0, x)
            self.y = random.randint(0, y)
        else :
            self.x = x
            self.y = y

    def rotate(self, angle):
        """Rotate the vector by the given angle in radians."""
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        new_x = self.x * cos_theta - self.y * sin_theta
        new_y = self.x * sin_theta + self.y * cos_theta
        self.x = new_x
        self.y = new_y

    def normalize(self):
        """Normalize the vector to unit length."""
        magnitude = math.sqrt(self.x ** 2 + self.y ** 2)
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude

    def __add__(self, other):
        """Add two Vect2D objects together."""
        if isinstance(other, Vect2D):
            return Vect2D(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +: 'Vect2D' and '{}'".format(type(other).__name__))

    def __mul__(self, other):
        """Multiply the vector by a scalar or another Vect2D object."""
        if isinstance(other, (int, float)):
            return Vect2D(self.x * other, self.y * other)
        elif isinstance(other, Vect2D):
            return Vect2D(self.x * other.x, self.y * other.y)
        else:
            raise TypeError("Unsupported operand type for *: 'Vect2D' and '{}'".format(type(other).__name__))

    def __truediv__(self, other):
        """Divide the vector by a scalar or another Vect2D object."""
        if isinstance(other, (int, float)):
            return Vect2D(self.x / other, self.y / other)
        elif isinstance(other, Vect2D):
            return Vect2D(self.x / other.x, self.y / other.y)
        else:
            raise TypeError("Unsupported operand type for /: 'Vect2D' and '{}'".format(type(other).__name__))

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def valueOnGrid(self, grid) :
        return grid[self.y][self.x]
        

