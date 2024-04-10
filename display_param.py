import tkinter as tk

class Display_param(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Paramétrage de la fourmi")
        self.geometry("1200x1000")
        self.resizable(height = False, width = False)
    
        self.widgets_creation()

    def widgets_creation(self):
        self.top_zone = tk.Frame(self)
        self.top_zone.pack(side="top", fill='x')
        self.top_zone['borderwidth'] = 2
        self.top_zone['relief'] = 'raised'

        self.left_zone = tk.Frame(self)
        self.left_zone.pack(side='left')
        self.left_zone['borderwidth'] = 2
        self.left_zone['relief'] = 'raised'

        self.lbl_message = tk.Label(self.top_zone, text = "Message :", font='Helvetica 12 bold')
        self.lbl_message.pack(side = tk.LEFT)

        self.txt_entry = tk.Entry(self.top_zone)
        self.txt_entry.pack()

        self.button_verr = tk.Button(self.top_zone, text="Verrouiler les paramètres")
        self.button_verr.pack(side = tk.RIGHT)
        self.button_verr.bind('<Button-1>', self.recover)

        self.lbl_message2 = tk.Label(self.left_zone, text = "Message 2 :", font='Helvetica 12 bold')
        self.lbl_message2.pack(side="top", anchor = "w")

        self.val_sens_offset_dist = tk.DoubleVar()
        self.sens_offset_dist = tk.Scale(self.left_zone, length=400, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur SENSOR OFFSET DISTANCE', variable= self.val_sens_offset_dist)
        self.sens_offset_dist.pack(fill = 'x')

        self.val_sens_size = tk.DoubleVar()
        self.sens_size = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur SENSOR SIZE', variable= self.val_sens_size)
        self.sens_size.pack(fill = 'x')

        self.val_sens_angle = tk.DoubleVar()
        self.sens_angle = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur SENSOR ANGLE', variable= self.val_sens_angle)
        self.sens_angle.pack(fill = 'x')

        self.val_turn_spd = tk.DoubleVar()
        self.turn_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur TURN SPEED', variable= self.val_turn_spd)
        self.turn_spd.pack(fill = 'x')

        self.val_mv_spd = tk.DoubleVar()
        self.mv_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur MOVE SPEED', variable= self.val_mv_spd)
        self.mv_spd.pack(fill = 'x')

        self.canevas = tk.Canvas(self, background='light blue', width=800 , height=800)
        self.canevas.pack(anchor="se")

    def recover(self, event):
        self.SENSOR_OFFSET_DISTANCE = self.val_sens_offset_dist.get()
        self.SENSOR_SIZE = self.val_sens_size.get()
        self.SENSOR_ANGLE_DEGREES = self.val_sens_angle.get()
        self.TURN_SPEED = self.val_turn_spd.get()
        self.MOVE_SPEED = self.val_mv_spd.get()

        print(f'offset : {self.SENSOR_OFFSET_DISTANCE}, size : {self.SENSOR_SIZE}, angle : {self.SENSOR_ANGLE_DEGREES}, turn : {self.TURN_SPEED}, move : {self.MOVE_SPEED}')



if __name__ == "__main__":
    app = Display_param()
    app.mainloop()