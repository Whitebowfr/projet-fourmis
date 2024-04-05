import tkinter as tk
import time
import numpy as np
from PIL import ImageTk, Image

class main(tk.Tk) :

    def __init__(self, width, height) :
        super().__init__()
        self.title("Test App")
        self.resizable(height = False, width = False)
        self.geometry("1000x1000")
        self.width = width
        self.height = height
        self.image = tk.PhotoImage(width=self.width, height=self.height)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.create_image((0, 0), image=self.image, anchor='nw')
        self.prev_time = time.time()
        self.i = 0
        self.grid = np.zeros([self.height, self.width, 3])
        self.ants = []
        

    def update_window(self) :
        PPMimage = f'P6 {self.grid.shape[1]} {self.grid.shape[0]} 255 '.encode() + np.array(self.grid, dtype=np.int8).tobytes()
        TKPimage = tk.PhotoImage(width=self.grid.shape[1], height=self.grid.shape[0], data=PPMimage, format='PPM')
        if hasattr(self.canvas, 'dummy_image_reference'): self.canvas.itemconfig(1, image=TKPimage)
        else: 
            self.canvas.create_image(self.canvas.winfo_width(), self.canvas.winfo_height()//3, image=TKPimage, anchor=tk.NW)
            self.canvas.dummy_image_reference = TKPimage # prevents garbage collecting of the PhotoImage object
        self.update_idletasks()
        self.update()
    
    def update_grid(self, grid, ants, updateWindow = True) :
        self.grid = grid
        self.ants = ants
        if updateWindow :
            self.update_window()

if __name__ == '__main__' :
    app = main(1000,1000)
    while True :
        app.update_window()
        a = np.random.randint(low=255, size=(100, 100, 3), dtype=np.uint8) # Original
        app.update_grid(a, [])