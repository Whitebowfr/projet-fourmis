from time import sleep
import tkinter as tk
import numpy as np

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

        self.lbl_message = tk.Label(self.top_zone, text = "Gestion des paramètres pré-enregistré :", font='Helvetica 12 bold')
        self.lbl_message.pack(side = tk.LEFT)

        self.button_verr = tk.Button(self.top_zone, text="Verrouiler les paramètres")
        self.button_verr.pack(side = tk.RIGHT)
        self.button_verr.bind('<Button-1>', self.end)

        self.button_save = tk.Button(self.top_zone, text="Enregistre les paramètres")
        self.button_save.pack(side = tk.RIGHT)
        self.button_save.bind('<Button-1>', self.parameter_save)

        self.val_spread_rate = tk.DoubleVar()
        self.val_spread_rate.set(10)
        self.spread_rate = tk.Scale(self.left_zone, length=400, orient = 'horizontal', from_= 0, to = 50, resolution = 1, tickinterval=10, label='Valeur spread RATE', variable= self.val_spread_rate)                 
        self.spread_rate.pack(side ='bottom', fill = 'x')

        self.val_decay_rate = tk.DoubleVar()
        self.val_decay_rate.set(0.5)
        self.decay_rate = tk.Scale(self.left_zone, length=400, orient = 'horizontal', from_= 0, to = 5, resolution = 0.25, tickinterval=1, label='Valeur DECAY RATE', variable= self.val_decay_rate)                 
        self.decay_rate.pack(side ='bottom', fill = 'x')

        self.val_sens_offset_dist = tk.DoubleVar()
        self.val_sens_offset_dist.set(2)
        self.sens_offset_dist = tk.Scale(self.left_zone, length=400, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur SENSOR OFFSET DISTANCE', variable= self.val_sens_offset_dist)                 
        self.sens_offset_dist.pack(side ='bottom', fill = 'x')

        self.val_sens_size = tk.DoubleVar()
        self.val_sens_size.set(45)
        self.sens_size = tk.Scale(self.left_zone, orient = 'horizontal', from_= 5, to = 90, resolution = 1, tickinterval=10, label='Valeur SENSOR SIZE', variable= self.val_sens_size)
        self.sens_size.pack(side ='bottom', fill = 'x')

        self.val_sens_angle = tk.DoubleVar()
        self.val_sens_angle.set(45)
        self.sens_angle = tk.Scale(self.left_zone, orient = 'horizontal', from_= 5, to = 90, resolution = 1, tickinterval=10, label='Valeur SENSOR ANGLE', variable= self.val_sens_angle)
        self.sens_angle.pack(side ='bottom', fill = 'x')

        self.val_turn_spd = tk.DoubleVar()
        self.val_turn_spd.set(150)
        self.turn_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 10, to = 300, resolution = 1, tickinterval=20, label='Valeur TURN SPEED', variable= self.val_turn_spd)
        self.turn_spd.pack(side ='bottom', fill = 'x')

        self.val_mv_spd = tk.DoubleVar()
        self.val_mv_spd.set(150)
        self.mv_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 10, to = 300, resolution = 1, tickinterval=40, label='Valeur MOVE SPEED', variable= self.val_mv_spd)
        self.mv_spd.pack(side ='bottom', fill = 'x')

        self.canevas = tk.Canvas(self, background='ivory', width=800 , height=500, scrollregion=(0, 0, 1600, 500), xscrollincrement=8)
        self.canevas.pack(anchor="se")
        self.gauche = True

        self.lbl_message2 = tk.Label(self.left_zone, text = "Réglages modifiables :", font='Helvetica 12 bold')
        self.lbl_message2.pack(side ='left', anchor = "nw")

        self.button_scro = tk.Button(self.left_zone, text="Défile l'affichage")
        self.button_scro.pack(side ='right', anchor = "ne")
        self.button_scro.bind('<Button-1>', self.scroll)

        self.display_canvas()
        self.refresh()

    def recover(self):
        list_chgt = []
        self.SENSOR_OFFSET_DISTANCE = int(self.val_sens_offset_dist.get())
        self.SENSOR_SIZE = int(self.val_sens_size.get())
        self.SENSOR_ANGLE_DEGREES = int(self.val_sens_angle.get())
        self.TURN_SPEED = int(self.val_turn_spd.get())
        self.MOVE_SPEED = int(self.val_mv_spd.get())
        self.SENSOR_DECAY_RATE = int(self.val_decay_rate.get())
        self.SENSOR_SPREAD_RATE = int(self.val_spread_rate.get())
        new_list = [self.SENSOR_OFFSET_DISTANCE, self.SENSOR_SIZE, self.SENSOR_ANGLE_DEGREES, self.TURN_SPEED, self.MOVE_SPEED, self.SENSOR_DECAY_RATE, self.SENSOR_SPREAD_RATE]
        if self.list_param:
            for i in range(len(self.list_param)):
                if new_list[i] != self.list_param[i]:
                    list_chgt.append(i)
        if 0 in list_chgt:
            self.anc_val_sensor_offset = self.list_param[0]
        self.list_param = new_list

        return list_chgt

    def display_canvas(self):
        self.recover()
        self.canevas.create_image([400, 250], image=self.img_fourmi)
        
        self.id_arc_av = self.canevas.create_arc([600-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 257-self.SENSOR_SIZE], [600+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 257+self.SENSOR_SIZE], extent=self.SENSOR_SIZE, start= -int(self.SENSOR_SIZE/2), fill='red')
        self.id_arc_g = self.canevas.create_arc([600-self.SENSOR_SIZE, 257-self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE], [600+self.SENSOR_SIZE, 257+self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE], extent=self.SENSOR_SIZE, start= self.SENSOR_ANGLE_DEGREES-int(self.SENSOR_SIZE/2), fill='red')
        self.id_arc_d = self.canevas.create_arc([600-self.SENSOR_SIZE, 257-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE], [600+self.SENSOR_SIZE, 257+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE], extent=-self.SENSOR_SIZE, start = -self.SENSOR_ANGLE_DEGREES+int(self.SENSOR_SIZE/2), fill='red')

        self.mv_arrow = self.canevas.create_line(400-self.MOVE_SPEED, 10, 400+self.MOVE_SPEED, 10, width=8, arrow='both')
        self.turn_arrow = self.canevas.create_line(400-self.TURN_SPEED, 400, 400, 495, 400+self.TURN_SPEED, 400, smooth='true', width=8, arrow='both')

        self.maison = self.canevas.create_rectangle([1000, 200],[1100, 300], fill='red')

    def refresh(self):
        list_chgt = self.recover()

        if 0 in list_chgt or 1 in list_chgt or 2 in list_chgt: 
            self.canevas.itemconfigure(self.id_arc_av, extent=self.SENSOR_SIZE, start=-int(self.SENSOR_SIZE/2))
            self.canevas.itemconfigure(self.id_arc_g, extent=self.SENSOR_SIZE, start=self.SENSOR_ANGLE_DEGREES-int(self.SENSOR_SIZE/2))
            self.canevas.itemconfigure(self.id_arc_d, extent=-self.SENSOR_SIZE, start=-self.SENSOR_ANGLE_DEGREES+int(self.SENSOR_SIZE/2))
            self.canevas.coords(self.id_arc_av, 600-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 257-self.SENSOR_SIZE, 600+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 257+self.SENSOR_SIZE)
            self.canevas.coords(self.id_arc_g, 600-self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 257-self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE-int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 600+self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 257+self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE-int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)))
            self.canevas.coords(self.id_arc_d, 600-self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 257-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE+int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 600+self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 257+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE+int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)))
        if 3 in list_chgt :
            self.canevas.coords(self.turn_arrow, 400-self.TURN_SPEED, 400, 400, 495, 400+self.TURN_SPEED, 400)
        if 4 in list_chgt :
            self.canevas.coords(self.mv_arrow, 400-self.MOVE_SPEED, 10, 400+self.MOVE_SPEED, 10)
        
        self.after(100, self.refresh)

    def scroll(self, event):
        self.xscroll(0)

    def xscroll(self, i):
        if self.gauche:
            if i<100:
                self.canevas.xview_scroll(1, "units")
                i+=1
                self.after(1, self.xscroll, i)
            else:
                self.gauche=False
        else:
            if i <100:
                self.canevas.xview_scroll(-1,"units")
                i+=1
                self.after(1, self.xscroll, i)
            else:
                self.gauche=True

    def parameter_save(self, event):
        pass

    def end(self, event):
        self.recover()
        print(f'offset : {self.SENSOR_OFFSET_DISTANCE}, size : {self.SENSOR_SIZE}, angle : {self.SENSOR_ANGLE_DEGREES}, turn : {self.TURN_SPEED}, move : {self.MOVE_SPEED}')
        self.quit()

if __name__ == "__main__":
    app = Display_param()
    app.mainloop()