from threading import Timer
from time import *
from fourmi import Fourmi

class pheromone:

    def __init__(self):
        self.positions = []
        self.temps = []
        self.intens = []
        self.types = []
        self.duree_de_vie = 10

    def ajoute(self, fourmi):
        self.positions.append((fourmi.x, fourmi.y))
        self.temps.append(time())
        self.intens.append(100)
        self.type()

    def types(self):
        self.type.append()

    def intensite(self):
        t_calcul = time()
        supp = 0
        for i in range(len(self.temps)):
            duree = t_calcul - self.temps[i]
            self.intens[i] = 100*(1-duree/self.duree_de_vie)
            if duree >= self.duree_de_vie:
                supp = i
        self.positions = self.positions[supp:]
        self.temps = self.temps[supp:]
        self.intens = self.intens[supp:]
        


"""
class MonTimer:
    # Le constructeur avec comme arguments le délai et la fonction à répéter
    def __init__(self, delai, fonction ):
        self.delai = delai
        self.fonction = fonction
        self.timer = Timer(delai, self.run) # création du Timer
        # Lors de l’appel à start, elle lance le Timer
    def start(self):
        self.timer.start()
    # A son exécution, elle relance le Timer pour qu’elle se répéte
    def run(self):
        self.timer = Timer(self.delai , self.run)
        self.timer.start()
        self.fonction()
    # Lors de l’appel à cancel, le Timer s’arrête
    def cancel(self):
        self.timer.cancel() """