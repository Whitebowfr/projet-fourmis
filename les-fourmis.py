class fourmi:

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    
    def avancer(self):
        if self.direction == 'N':
            self.y -= 1
        elif self.direction == 'S':
            self.y += 1
        elif self.direction == 'E':
            self.x += 1
        elif self.direction == 'O':
            self.x -= 1
    
    def tourner(self, sens):
        if sens == 'D':
            if self.direction == 'N':
                self.direction = 'E'
            elif self.direction == 'E':
                self.direction = 'S'
            elif self.direction == 'S':
                self.direction = 'O'
            elif self.direction == 'O':
                self.direction = 'N'
        elif sens == 'G':
            if self.direction == 'N':
                self.direction = 'O'
            elif self.direction == 'O':
                self.direction = 'S'
            elif self.direction == 'S':
                self.direction = 'E'
            elif self.direction == 'E':
                self.direction = 'N'
