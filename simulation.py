from Environnement import Environment
from display import Display
from ants import Ants
import taichi as ti
import time
import constants

@ti.data_oriented
class FourmiSim:
    def __init__(self, width, height, N):
        self.env = Environment(width, height, "./saved_images/output.png")#"./saved_images/output.png"
        self.ants = Ants(N, self.env.grid, self.env.home, self.env.food)
        #ti.sync()
        self.display = Display(width, height, self.env.home)

        self.i = 0
        self.updateFourmis(0.1)
        ti.sync()
        self.display.update_grid(self.env.grid, self.ants.positions, self.env.food)
        ti.sync()

    def update_game(self):
        deltaT = time.time() - self.previous_update
        self.previous_update = time.time()
        self.env.decay(deltaT)
        if self.i % ti.static(constants.SPREAD_RATE) == 0:
            self.env.box_blur()
        self.updateFourmis(deltaT)
        self.display.update_grid(self.env.grid, self.ants.positions, self.env.food)
        self.i += 1
    
    def updateFourmis(self, deltaT:float) :
        self.ants.update(deltaT)


    def run(self) :
        self.previous_update = time.time()
        while self.display.gui.running:
            self.update_game()
            ti.sync()

    def runStep(self):
        self.update_game()
    

if __name__ == "__main__":
    ti.init(arch=ti.vulkan)
    sim = FourmiSim(700, 700, 2000)
    sim.run()
            