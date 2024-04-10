import tkinter as tk
import time
import numpy as np

class Display(tk.Tk) :

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
        self.grid = np.zeros([self.height, self.width])
        self.ants = []
        

    def update_window(self):
        grayscale_array = self.convert_to_grayscale(self.grid)
        hex_array = self.convert_to_hex(grayscale_array)
        str = ' '.join('{' + ' '.join(row) + '}' for row in hex_array)

        self.image.put(str, to=(0, 0))
        self.update_idletasks()
        self.update()

    def convert_to_hex(self, array):
        # Create a new 2D array for hex values
        hex_array = [['#000000'] * len(array[0]) for _ in range(len(array))]

        # Iterate over each pixel in the array and calculate the hex value
        for y in range(len(array)):
            for x in range(len(array[y])):
                r, g, b = array[y][x]
                hex_value = '#{:02x}{:02x}{:02x}'.format(r, g, b)  # Convert to hex value
                hex_array[y][x] = hex_value

        return hex_array

    def convert_to_grayscale(self, array):
            # Create a new 2D array for grayscale values
        grayscale_array = [[0] * len(array[0]) for _ in range(len(array))]

            # Iterate over each pixel in the array and calculate the grayscale value
        for y in range(len(array)):
            for x in range(len(array[y])):
                pixel_value = array[y][x]
                grayscale_value = int(pixel_value * 255 / 255)  # Convert to grayscale value
                grayscale_array[y][x] = (grayscale_value, grayscale_value, grayscale_value)

        return grayscale_array

    def update_grid(self, grid, ants, updateWindow = True) :
        self.grid = grid
        self.ants = ants
        if updateWindow :
            self.update_window()

if __name__ == '__main__' :
    app = Display(1000,1000)
    while True :
        a = np.random.randint(0, 255, (1000, 1000))
        app.update_grid(a, [])