import tkinter as tk
from paint_taichi import Paint
from simulation import FourmiSim
import taichi as ti

from display_set import Display_param

ti.init(arch=ti.vulkan)

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu principal")
        self.geometry('500x200')

        # Create the buttons
        self.text = tk.Label(self, text="Bienvenue dans la simulation de fourmis !")
        self.button1 = tk.Button(self, text="Lancer la simulation", command=self.button1_action)
        self.button2 = tk.Button(self, text="Changer les paramètres", command=self.button2_action)
        self.button3 = tk.Button(self, text="Créer une carte", command=self.button3_action)
        self.button4 = tk.Button(self, text="Quitter", command=self.quit)

        # Pack the buttons
        self.text.pack(expand=True)
        self.button1.pack(ipadx=3, ipady=3)
        self.button2.pack(ipadx=3, ipady=3)
        self.button3.pack(ipadx=3, ipady=3)
        self.button4.config(fg='red')
        self.button4.pack(ipadx=3, ipady=3, expand=True)

    def button1_action(self):
        FourmiSim(700, 700, 1000).run()

    def button2_action(self):
        Display_param().mainloop()

    def button3_action(self):
        Paint(700,700).run()

# Create an instance of the MainMenu class
menu = MainMenu()

# Start the Tkinter event loop
menu.mainloop()
