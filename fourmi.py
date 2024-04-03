class fourmi:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    
    def update(self, environnement):
        


        if environnement[self.x][self.y] == 0:
            environnement[self.x][self.y] = 1
            self.x += 1
        else:
            pass

        

        