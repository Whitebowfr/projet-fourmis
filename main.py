from Environnement import Environment
from Vectors import Vect2D
from display import Display
from ants import Ants
import taichi as ti
import time

class FourmiSim :
    def __init__(self, width, height, N) :
        self.env = Environment(width, height)
        self.display = Display(width, height)
        self.size = Vect2D(width, height)
        self.previous_update = time.time()
        self.i = 0
        self.ants = Ants(N, self.env.grid)
        self.display.update_grid(self.env.grid, self.ants)

    def update_game(self) :
        deltaT = time.time() - self.previous_update
        self.previous_update = time.time()
        self.env.decay(deltaT)
        self.env.box_blur(deltaT)
        self.updateFourmis(deltaT)
        ti.sync()
        self.display.update_grid(self.env.grid, self.ants)
        self.i += 1
    
    def updateFourmis(self, deltaT:float) :
        self.ants.update(deltaT)

    def run(self) :
        while True :
            self.update_game()

    def runStep(self):
        self.update_game()
    

if __name__ == "__main__" :
    sim = FourmiSim(1000, 1000, 1000)
    sim.run()
            