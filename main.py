from Environnement import Environment
from fourmi import fourmi
from Vectors import Vect2D
from display import Display
import taichi as ti
import random
import time

ti.init(arch=ti.cpu)

@ti.data_oriented
class FourmiSim :
    def __init__(self, width, height) :
        self.env = Environment(width, height)
        self.display = Display(width, height)
        self.size = Vect2D(width, height)
        self.display.update_grid(self.env.grid, self.env.fourmis)
        self.init_fourmis()
        self.previous_update = time.time()
        self.i = 0

    def init_fourmis(self) :
        for _ in range(200) :
            self.env.addFourmi(fourmi(ti.Vector([random.randint(0, self.size.x), random.randint(0, self.size.y)])))

    def update_game(self) :
        deltaT = time.time() - self.previous_update
        self.previous_update = time.time()
        self.env.decay(deltaT)
        self.updateFourmis(deltaT)
        ti.sync()
        self.display.update_grid(self.env.grid, self.env.fourmis)
        self.i += 1
    
    @ti.kernel
    def updateFourmis(self, deltaT:float) :
        for ant in self.env.fourmis :
            ant.update(self.env.grid, deltaT, self.i)

    def run(self) :
        while True :
            self.update_game()

    def runStep(self):
        self.update_game()
    

if __name__ == "__main__" :
    sim = FourmiSim(400, 400)
    sim.run()
            