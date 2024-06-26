import tkinter as tk

class Display_param(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Paramétrage de la fourmi")
        self.geometry("1200x550")
        self.resizable(height = False, width = False)
    
        self.img_fourmi = tk.PhotoImage(file="fourmi.png")
        self.list_param = [2, 3, 45, 15, 15]
        self.anc_val_sensor_offset = self.list_param[0]

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
        self.txt_entry.pack(side = tk.BOTTOM)

        self.button_verr = tk.Button(self.top_zone, text="Verrouiler les paramètres")
        self.button_verr.pack(side = tk.RIGHT)
        self.button_verr.bind('<Button-1>', self.end)

        self.lbl_message2 = tk.Label(self.left_zone, text = "Message 2 :", font='Helvetica 12 bold')
        self.lbl_message2.pack(side="top", anchor = "w")

        self.val_sens_offset_dist = tk.DoubleVar()
        self.val_sens_offset_dist.set(2)
        self.sens_offset_dist = tk.Scale(self.left_zone, length=400, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur SENSOR OFFSET DISTANCE', variable= self.val_sens_offset_dist)
                                         
        self.sens_offset_dist.pack(fill = 'x')

        self.val_sens_size = tk.DoubleVar()
        self.val_sens_size.set(3)
        self.sens_size = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur SENSOR SIZE', variable= self.val_sens_size)
        self.sens_size.pack(fill = 'x')

        self.val_sens_angle = tk.DoubleVar()
        self.val_sens_angle.set(45)
        self.sens_angle = tk.Scale(self.left_zone, orient = 'horizontal', from_= 5, to = 45, resolution = 1, tickinterval=5, label='Valeur SENSOR ANGLE', variable= self.val_sens_angle)
        self.sens_angle.pack(fill = 'x')

        self.val_turn_spd = tk.DoubleVar()
        self.val_turn_spd.set(15)
        self.turn_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur TURN SPEED', variable= self.val_turn_spd)
        self.turn_spd.pack(fill = 'x')

        self.val_mv_spd = tk.DoubleVar()
        self.val_mv_spd.set(15)
        self.mv_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur MOVE SPEED', variable= self.val_mv_spd)
        self.mv_spd.pack(fill = 'x')

        self.canevas = tk.Canvas(self, background='light blue', width=800 , height=500)
        self.canevas.pack(anchor="se")

        self.display_canvas()
        self.refresh()

    def recover(self):
        list_chgt = []
        self.SENSOR_OFFSET_DISTANCE = int(self.val_sens_offset_dist.get())
        self.SENSOR_SIZE = int(self.val_sens_size.get())
        self.SENSOR_ANGLE_DEGREES = int(self.val_sens_angle.get())
        self.TURN_SPEED = int(self.val_turn_spd.get())
        self.MOVE_SPEED = int(self.val_mv_spd.get())
        new_list = [self.SENSOR_OFFSET_DISTANCE, self.SENSOR_SIZE, self.SENSOR_ANGLE_DEGREES, self.TURN_SPEED, self.MOVE_SPEED]
        if self.list_param:
            for i in range(len(self.list_param)):
                if new_list[i] != self.list_param[i]:
                    list_chgt.append(i)
        if 0 in list_chgt:
            self.anc_val_sensor_offset = self.list_param[0]
        self.list_param = new_list

        return list_chgt

    def display_canvas(self):
        list_chgt = self.recover()
        self.canevas.create_image([400, 250], image=self.img_fourmi)
        
        self.id_arc_av = self.canevas.create_arc([500+self.SENSOR_OFFSET_DISTANCE, 157], [700+self.SENSOR_OFFSET_DISTANCE, 357], extent=2*self.SENSOR_ANGLE_DEGREES, start= -self.SENSOR_ANGLE_DEGREES, fill='red')
        self.id_arc_g = self.canevas.create_arc([500, 157-self.SENSOR_OFFSET_DISTANCE], [700, 357-self.SENSOR_OFFSET_DISTANCE], extent=2*self.SENSOR_ANGLE_DEGREES, start= 90-self.SENSOR_ANGLE_DEGREES, fill='red')
        self.id_arc_d = self.canevas.create_arc([500, 157+self.SENSOR_OFFSET_DISTANCE], [700, 357+self.SENSOR_OFFSET_DISTANCE], extent=2*self.SENSOR_ANGLE_DEGREES, start = 270-self.SENSOR_ANGLE_DEGREES, fill='red')

        self.mv_arrow = self.canevas.create_line(10,10, 110,10, width=5, arrow='both')
        self.turn_arrow = self.canevas.create_line(10,400, 55,495, 110,400, smooth='true', width=5, arrow='both')

    def refresh(self):
        list_chgt = self.recover()

        if 0 in list_chgt:
            self.canevas.move(self.id_arc_av, self.SENSOR_OFFSET_DISTANCE-self.anc_val_sensor_offset, 0)
            self.canevas.move(self.id_arc_g, 0, -(self.SENSOR_OFFSET_DISTANCE-self.anc_val_sensor_offset))
            self.canevas.move(self.id_arc_d, 0, self.SENSOR_OFFSET_DISTANCE-self.anc_val_sensor_offset)
        if 1 in list_chgt:
            self.canevas.itemconfigure(self.id_arc_av)
            self.canevas.itemconfigure(self.id_arc_g)
            self.canevas.itemconfigure(self.id_arc_d)
        if 2 in list_chgt:
            self.canevas.itemconfigure(self.id_arc_av, extent=2*self.SENSOR_ANGLE_DEGREES, start=-self.SENSOR_ANGLE_DEGREES)
            self.canevas.itemconfigure(self.id_arc_g, extent=2*self.SENSOR_ANGLE_DEGREES, start=90-self.SENSOR_ANGLE_DEGREES)
            self.canevas.itemconfigure(self.id_arc_d, extent=2*self.SENSOR_ANGLE_DEGREES, start=270-self.SENSOR_ANGLE_DEGREES)

        self.after(100, self.refresh)

    def end(self, event):
        self.recover()
        print(f'offset : {self.SENSOR_OFFSET_DISTANCE}, size : {self.SENSOR_SIZE}, angle : {self.SENSOR_ANGLE_DEGREES}, turn : {self.TURN_SPEED}, move : {self.MOVE_SPEED}')
        self.quit()

if __name__ == "__main__":
    app = Display_param()
    app.mainloop()