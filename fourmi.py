import math

class fourmi:

    def __init__(self, x, y, vit_x = 1, vit_y = 0):
        self.x = x
        self.y = y
        self.vit_x = vit_x
        self.vit_y = vit_y
        self.acc_x = 0
        self.acc_y = 0

        self.a_nourriture = False
    
    def update(self, environnement):
        

        self.acc_x = 0 # formule en fonction de l'environnement
        self.acc_y = 0 # formule en fonction de l'environnement

        for i in range(-5,5):
            for j in range(-3,3):
                # TODO : formule en fonction de l'environnement
                pass
        self.vit_x += self.acc_x
        self.vit_y += self.acc_y

        if math.sqrt(self.vit_x**2 + self.vit_y**2) > 1:
            self.vit_x = self.vit_x / math.sqrt(self.vit_x**2 + self.vit_y**2)
            self.vit_y = self.vit_y / math.sqrt(self.vit_x**2 + self.vit_y**2)


        self.x += self.vit_x
        self.y += self.vit_y

        environnement.addPhero # TODO : bon format en fonction de l'environnement

        

        