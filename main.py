from Environnement import Environment
from fourmi import fourmi
from Vectors import Vect2D
from display import Display
import time

class FourmiSim :
    def __init__(self, width, height) :
        self.env = Environment(width, height)
        self.display = Display(width, height)
        self.size = Vect2D(width, height)
        self.display.update_grid(self.env.grid, self.env.fourmis)
        self.init_fourmis()
        self.previous_update = time.time()

    def init_fourmis(self) :
        for _ in range(20) :
            self.env.addFourmi(fourmi(Vect2D(self.size.x // 2, self.size.y // 2, randomPos=True)))

    def update_game(self) :
        deltaT = time.time() - self.previous_update
        self.previous_update = time.time()
        self.env.decay(deltaT)
        for ant in self.env.fourmis :
            ant.update(self.env, deltaT)
        self.display.update_grid(self.env.grid, self.env.fourmis)
        print("deltaT : ", deltaT)

    def run(self) :
        while True :
            self.update_game()

    def runStep(self):
        self.update_game()
    

if __name__ == "__main__" :
    sim = FourmiSim(1000, 1000)
    sim.run()
            