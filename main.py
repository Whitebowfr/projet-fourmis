from Environnement import Environment
from display import Display
from ants import Ants
import taichi as ti
import time

ti.init()

class FourmiSim :
    def __init__(self, width, height, N) :
        self.env = Environment(width, height, 2)
        self.ants = Ants(N, self.env.grid, self.env.home, self.env.food)
        ti.sync()
        self.display = Display(width, height, 2, self.env.home)
        self.previous_update = time.time()
        self.i = 0
        ti.sync()
        self.display.update_grid(self.env.grid, self.ants, self.env.food)

    def update_game(self) :
        deltaT = time.time() - self.previous_update
        self.previous_update = time.time()
        self.env.decay(deltaT)
        if self.i % 10 == 0 :
            self.env.box_blur()
        self.updateFourmis(deltaT)
        ti.sync()
        self.display.update_grid(self.env.grid, self.ants, self.env.food)
        self.i += 1
    
    def updateFourmis(self, deltaT:float) :
        self.ants.update(deltaT)

    def run(self) :
        while True :
            self.update_game()

    def runStep(self):
        self.update_game()
    

if __name__ == "__main__" :
    sim = FourmiSim(700, 700, 500)
    sim.run()
            