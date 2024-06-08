import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
import numpy as np
import csv
import random
import constants as c

class Display_set(tk.Toplevel):

    def __init__(self):
        """
        Initialisation de la fenêtre de paramètres 
        Input, output : None
        """
        # Création de la fenêtre tkinter

        super().__init__()
        self.title("Paramétrage de la fourmi")
        self.geometry("1250x640")
        self.resizable(height = False, width = False)
    
        # Importation des images et CSV

        self.img_fourmi = tk.PhotoImage(file="fourmi.png")
        self.img_fourmi2 = tk.PhotoImage(file="fourmi2.png")
        self.list_param = [2]
        self.anc_val_sensor_offset = self.list_param[0]

        self.f_path = "parametres_fourmis_(default).csv"

        self.COLORS = {"fourmis": "#FF0000", 
                  "food": "#00FF00",
                  "maison": "#FFA500",
                  "obstacles": "#646464",
                  "pheromones": ["#FF0000", "#00FFFF"]}
        self.dico_color={}
        self.dico_nom = {"fourmis": "Fourmi", 
                  "food": "Nourriture",
                  "maison": "Maison",
                  "obstacles": "Obstacles",
                  "pheromones_0": "Phéromone sans nourriture",
                  "pheromones_1": "Phéromone avec nourriture"}

        
        # Lancement de l'affichage

        self.widgets_creation()
        self.refresh_menu_deroulant(None)

    def widgets_creation(self):
        """
        Affichage des widgets sur la fenêtre et lanacement de la création du canevas
        Input, outup : None
        """
        # Création des frames pour diviser la fenêtre

        self.top_zone = tk.Frame(self)
        self.top_zone.pack(side="top", fill='x')
        self.top_zone['borderwidth'] = 2
        self.top_zone['relief'] = 'raised'

        self.left_zone = tk.Frame(self)
        self.left_zone.pack(side='left')
        self.left_zone['borderwidth'] = 2
        self.left_zone['relief'] = 'raised'

        self.left_zone2 = tk.Frame(self)
        self.left_zone2.pack(side='left')
        self.left_zone2['borderwidth'] = 2
        self.left_zone2['relief'] = 'raised'

        # Création et placement des widgets dans la zone du dessus
        
        self.lbl_message = tk.Label(self.top_zone, text = "Gestion des paramètres pré-enregistré :", font='Helvetica 12 bold')
        self.lbl_message.grid(row=0, column=0, sticky='w')
        self.lbl_message = tk.Label(self.top_zone, text = "Valeur sélectionner :", font='Helvetica 12 bold')
        self.lbl_message.grid(row=1, column=0, sticky='e')


        self.texte = tk.StringVar()
        self.texte.set("Nom de la configuration à enregistrer")
        self.entry = tk.Entry(self.top_zone, textvariable=self.texte, width=30)
        self.entry.grid(row=0, column=1, sticky='w')

        self.menu_deroulant = ttk.Combobox(self.top_zone, values=[])
        self.menu_deroulant.grid(row=1, column=1, sticky='w')
        self.menu_deroulant.bind('<<ComboboxSelected>>', self.change_value)
        self.menu_deroulant.bind('<Button-1>', self.refresh_menu_deroulant)
        

        self.button_chose_file = tk.Button(self.top_zone, text="Choisir un fichier")
        self.button_chose_file.grid(row=0, column=2, sticky='w')
        self.button_chose_file.bind('<Button-1>', self.chose_file)

        self.button_suppr = tk.Button(self.top_zone, text="Supprimer la configuration")
        self.button_suppr.grid(row=1, column=2, sticky='w')
        self.button_suppr.bind('<Button-1>', self.supprimer_param)

        self.button_verr = tk.Button(self.top_zone, text="Verrouiller la configuration")
        self.button_verr.grid(row=1, column=4, sticky='w')
        self.button_verr.bind('<Button-1>', self.verr_param)

        self.button_save = tk.Button(self.top_zone, text="Enregistrer la configuration")
        self.button_save.grid(row=1, column=5, sticky='w')
        self.button_save.bind('<Button-1>', self.parameter_save)

        self.button_scro = tk.Button(self.top_zone, text="Défile l'affichage")
        self.button_scro.grid(row=1, column=6, sticky='w')
        self.button_scro.bind('<Button-1>', self.scroll)

        self.label_message = tk.Label(self.top_zone, text = "", font='Helvetica 12 bold')
        self.label_message.grid(row=0, column=4, sticky='w', columnspan=3)

        # Création et placement des widgets (curseurs) dans la zone 2 de gauche
        
        self.val_random_fact = tk.DoubleVar()
        self.val_random_fact.set(5)
        self.random_fact = tk.Scale(self.left_zone2, length=400, orient = 'horizontal', from_= 0, to = 15, resolution = 1, tickinterval=3, label='Valeur RANDOM FACT', variable= self.val_random_fact)                 
        self.random_fact.pack(side ='bottom', fill = 'x')

        self.val_food_count = tk.DoubleVar()
        self.val_food_count.set(12)
        self.food_count = tk.Scale(self.left_zone2, length=400, orient = 'horizontal', from_= 1, to = 10, resolution = 1, tickinterval=2, label='Valeur FOOD COUNT', variable= self.val_food_count)                 
        self.food_count.pack(side ='bottom', fill = 'x')

        self.val_food_size = tk.DoubleVar()
        self.val_food_size.set(10)
        self.food_size = tk.Scale(self.left_zone2, length=400, orient = 'horizontal', from_= 5, to = 100, resolution = 1, tickinterval=19, label='Valeur FOOD SIZE', variable= self.val_food_size)                 
        self.food_size.pack(side ='bottom', fill = 'x')

        self.val_home_size = tk.DoubleVar()
        self.val_home_size.set(10)
        self.home_size = tk.Scale(self.left_zone2, length=400, orient = 'horizontal', from_= 5, to = 100, resolution = 1, tickinterval=19, label='Valeur HOME SIZE', variable= self.val_home_size)                 
        self.home_size.pack(side ='bottom', fill = 'x')

        self.val_spread_rate = tk.DoubleVar()
        self.val_spread_rate.set(1)
        self.spread_rate = tk.Scale(self.left_zone2, length=400, orient = 'horizontal', from_= 0, to = 10, resolution = 0.1, tickinterval=2, label='Valeur SPREAD RATE', variable= self.val_spread_rate)                 
        self.spread_rate.pack(side ='bottom', fill = 'x')

        self.val_decay_rate = tk.DoubleVar()
        self.val_decay_rate.set(0.5)
        self.decay_rate = tk.Scale(self.left_zone2, length=400, orient = 'horizontal', from_= 0, to = 5, resolution = 0.1, tickinterval=1, label='Valeur DECAY RATE', variable= self.val_decay_rate)                 
        self.decay_rate.pack(side ='bottom', fill = 'x')
        
        self.left_zone2.pack_forget() # On masque le cadre de gauche 2

        # Création et placement des widgets (curseurs) dans la zone 1 de gauche
        
        self.val_sens_offset_dist = tk.DoubleVar()
        self.val_sens_offset_dist.set(2)
        self.sens_offset_dist = tk.Scale(self.left_zone, length=400, orient = 'horizontal', from_= 0, to = 100, resolution = 1, tickinterval=20, label='Valeur SENSOR OFFSET DISTANCE', variable= self.val_sens_offset_dist)                 
        self.sens_offset_dist.pack(side ='bottom', fill = 'x')

        self.val_sens_size = tk.DoubleVar()
        self.val_sens_size.set(45)
        self.sens_size = tk.Scale(self.left_zone, orient = 'horizontal', from_= 5, to = 90, resolution = 1, tickinterval=17, label='Valeur SENSOR SIZE', variable= self.val_sens_size)
        self.sens_size.pack(side ='bottom', fill = 'x')

        self.val_sens_angle = tk.DoubleVar()
        self.val_sens_angle.set(45)
        self.sens_angle = tk.Scale(self.left_zone, orient = 'horizontal', from_= 5, to = 90, resolution = 1, tickinterval=17, label='Valeur SENSOR ANGLE', variable= self.val_sens_angle)
        self.sens_angle.pack(side ='bottom', fill = 'x')

        self.val_lost_spd = tk.DoubleVar()
        self.val_lost_spd.set(0.3)
        self.lost_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 0, to = 1, resolution = 0.05, tickinterval=0.2, label='Valeur LOST SPEED', variable= self.val_lost_spd)
        self.lost_spd.pack(side ='bottom', fill = 'x')

        self.val_turn_spd = tk.DoubleVar()
        self.val_turn_spd.set(150)
        self.turn_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 10, to = 300, resolution = 1, tickinterval=58, label='Valeur TURN SPEED', variable= self.val_turn_spd)
        self.turn_spd.pack(side ='bottom', fill = 'x')

        self.val_mv_spd = tk.DoubleVar()
        self.val_mv_spd.set(150)
        self.mv_spd = tk.Scale(self.left_zone, orient = 'horizontal', from_= 10, to = 300, resolution = 1, tickinterval=58, label='Valeur MOVE SPEED', variable= self.val_mv_spd)
        self.mv_spd.pack(side ='bottom', fill = 'x')

        self.canevas = tk.Canvas(self, background='ivory', width=800 , height=600, scrollregion=(0, 0, 1600, 500), xscrollincrement=8)
        self.canevas.pack(anchor="e")
        self.gauche = True

        self.lbl_message2 = tk.Label(self.left_zone, text = "Réglages modifiables :", font='Helvetica 12 bold')
        self.lbl_message2.pack(side ='left', anchor = "nw")
        
        # On lance l'affichage des figures sur le canevas et le réfraichissement

        self.display_canvas()
        self.refresh()

    def recover(self):
        """
        Méthode permettant de récupérer les paramètres sélectionnés dans les curseurs
        Input : None
        Output : list_chgt, liste contenant les numéros des paramètres changés
        """
        # On récupère tous les paramètres des curseurs pour les stocker

        list_chgt = []
        self.SENSOR_OFFSET_DISTANCE = int(self.val_sens_offset_dist.get())
        self.SENSOR_SIZE = int(self.val_sens_size.get())
        self.SENSOR_ANGLE_DEGREES = int(self.val_sens_angle.get())
        self.TURN_SPEED = int(self.val_turn_spd.get())
        self.MOVE_SPEED = int(self.val_mv_spd.get())
        self.LOST_SPEED = float(self.val_lost_spd.get())
        self.DECAY_RATE = float(self.val_decay_rate.get())
        self.SPREAD_RATE = float(self.val_spread_rate.get())
        self.HOME_SIZE = int(self.val_home_size.get())
        self.FOOD_SIZE = int(self.val_food_size.get())
        self.FOOD_COUNT = int(self.val_food_count.get())
        self.RANDOM_FACT = int(self.val_random_fact.get())
        
        # On compare et on note quels parmètres ont été changés afin d'optimiser le réaffichage
       
        new_list = [self.SENSOR_OFFSET_DISTANCE, self.SENSOR_SIZE, self.SENSOR_ANGLE_DEGREES, self.TURN_SPEED, self.MOVE_SPEED, self.LOST_SPEED, self.DECAY_RATE, self.SPREAD_RATE, self.HOME_SIZE, self.FOOD_SIZE, self.FOOD_COUNT, self.RANDOM_FACT]
        if self.list_param:
            for i in range(len(self.list_param)):
                if new_list[i] != self.list_param[i]:
                    list_chgt.append(i)
        if 0 in list_chgt:
            self.anc_val_sensor_offset = self.list_param[0]
        self.list_param = new_list

        return list_chgt

    def display_canvas(self):
        """
        Affichage de tous les éléments du canevas et lancement des fonctions particulières d'affichage
        Input, output : None
        """
        # On récupère les paramètres et on affiche les formes souhaitées

        self.recover()
        self.canevas.create_image([350, 300], image=self.img_fourmi)
        
        self.id_arc_av = self.canevas.create_arc([550-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 307-self.SENSOR_SIZE], [550+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 307+self.SENSOR_SIZE], extent=self.SENSOR_SIZE, start= -int(self.SENSOR_SIZE/2), fill='red')
        self.id_arc_g = self.canevas.create_arc([550-self.SENSOR_SIZE, 307-self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE], [550+self.SENSOR_SIZE, 307+self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE], extent=self.SENSOR_SIZE, start= self.SENSOR_ANGLE_DEGREES-int(self.SENSOR_SIZE/2), fill='red')
        self.id_arc_d = self.canevas.create_arc([550-self.SENSOR_SIZE, 307-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE], [550+self.SENSOR_SIZE, 307+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE], extent=-self.SENSOR_SIZE, start = -self.SENSOR_ANGLE_DEGREES+int(self.SENSOR_SIZE/2), fill='red')

        self.mv_arrow = self.canevas.create_line(350-self.MOVE_SPEED, 10, 350+self.MOVE_SPEED, 10, width=8, arrow='both')
        self.turn_arrow = self.canevas.create_line(350-self.TURN_SPEED, 550, 350, 595, 350+self.TURN_SPEED, 550, smooth='true', width=8, arrow='both')

        self.lost_rect = self.canevas.create_rectangle(10, 400-200*self.LOST_SPEED, 30, 400, fill='red')
        self.cadre_lost_rect = self.canevas.create_rectangle(10, 200, 30, 400, width='2', outline='black')

        self.home = self.canevas.create_rectangle(950-self.HOME_SIZE, 105-self.HOME_SIZE,950+self.HOME_SIZE, 105+self.HOME_SIZE, fill=self.COLORS['maison'])
        self.txt_home = self.canevas.create_text(950, 105, text='Home', fill='white', font='Times '+str(int(self.HOME_SIZE/2))+' bold')
        self.food = self.canevas.create_oval(950-self.FOOD_SIZE, 310-self.FOOD_SIZE,950+self.FOOD_SIZE, 310+self.FOOD_SIZE, fill=self.COLORS['food'])
        self.txt_food = self.canevas.create_text(950, 310, text='Food', fill='white', font='Times '+str(int(self.FOOD_SIZE/2))+' bold')

        self.canevas.create_image([1300, 100], image=self.img_fourmi2)

        self.decay_rect = self.canevas.create_rectangle(1215, 95, 1225, 105, fill=self.COLORS['pheromones'][0], state='normal')
        self.decay_dis = True
        self.blink() # On lance le clignotement de la phéromone
        
        self.list_rect_spread = [[0 for i in range(9)] for j in range(9)]
        self.spread_val = -1
        self.spread_blink() # On lance le clignotement de propagation des phéromones
        for y in range(len(self.area_spread)):
            for x in range(len(self.area_spread[0])):
                self.rect_spread = self.canevas.create_rectangle(1100+10*x , 55+10*y, 1100+10*(x+1), 55+10*(y+1), fill=self.color(self.area_spread[y][x]))
                self.list_rect_spread[y][x]=self.rect_spread 

        self.list_oval_foods = [[None for j in range(5)] for i in range(2)]
        for y in range(2):
            for x in range(5):
                self.oval_food = self.canevas.create_oval(1100+100*x , 250+70*y, 1100+100*(x+1)-50, 250+70*(y+1)-20, fill=self.COLORS['food'], state='hidden')
                self.list_oval_foods[y][x]=self.oval_food 
        self.display_foods() # On affiche le nombre de nourritures

        self.rect_random = self.canevas.create_rectangle(811, 499, 1588, 526, width='2', outline='black')
        self.oval_random = self.canevas.create_oval(1187, 500, 1212, 525, fill='white')

        self.display_random() # On affiche le disque à une place aléatoire

        self.canevas.create_text(950, 450, text='Choix des couleurs : ', font='Times 25 bold')

        i = 0
        for form in self.COLORS.keys():
            if form != "pheromones":
                id = self.canevas.create_rectangle(1100+i*80, 425, 1150+i*80, 475, fill=self.COLORS[form])
                self.canevas.tag_bind(id, '<Button-1>', self.change_color)
                self.dico_color[id] = {'nom':form, 'color':self.COLORS[form]}
                self.canevas.create_text(1125+i*80, 400, text=self.dico_nom[form])
                i+=1
            else:
                id_0 = self.canevas.create_rectangle(1100+i*80, 425, 1150+i*80, 475, fill=self.COLORS[form][0])
                self.canevas.tag_bind(id_0, '<Button-1>', self.change_color)
                self.dico_color[id_0] = {'nom':form+'_0', 'color':self.COLORS[form][0]}
                self.canevas.create_text(1125+i*80, 415, text=self.dico_nom[form+'_0'])
                i+=1
                id_1 = self.canevas.create_rectangle(1100+i*80, 425, 1150+i*80, 475, fill=self.COLORS[form][1])
                self.canevas.tag_bind(id_1, '<Button-1>', self.change_color)
                self.dico_color[id_1] = {'nom':form+'_1', 'color':self.COLORS[form][1]}
                self.canevas.create_text(1125+i*80, 400, text=self.dico_nom[form+'_1'])

    def refresh(self):
        """
        Rafraichissemnt de l'affichage du canevas avec les paramètres en direct (toutes les 100ms)
        Input, output : None
        """
        list_chgt = self.recover()
    
        if 0 in list_chgt or 1 in list_chgt or 2 in list_chgt: 
            self.canevas.itemconfigure(self.id_arc_av, extent=self.SENSOR_SIZE, start=-int(self.SENSOR_SIZE/2))
            self.canevas.itemconfigure(self.id_arc_g, extent=self.SENSOR_SIZE, start=self.SENSOR_ANGLE_DEGREES-int(self.SENSOR_SIZE/2))
            self.canevas.itemconfigure(self.id_arc_d, extent=-self.SENSOR_SIZE, start=-self.SENSOR_ANGLE_DEGREES+int(self.SENSOR_SIZE/2))
            self.canevas.coords(self.id_arc_av, 550-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 307-self.SENSOR_SIZE, 550+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE, 307+self.SENSOR_SIZE)
            self.canevas.coords(self.id_arc_g, 550-self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 307-self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE-int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 550+self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 307+self.SENSOR_SIZE-self.SENSOR_OFFSET_DISTANCE-int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)))
            self.canevas.coords(self.id_arc_d, 550-self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 307-self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE+int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 550+self.SENSOR_SIZE+int(self.SENSOR_OFFSET_DISTANCE*np.cos(np.pi*self.SENSOR_ANGLE_DEGREES/180)), 307+self.SENSOR_SIZE+self.SENSOR_OFFSET_DISTANCE+int(self.SENSOR_OFFSET_DISTANCE*np.sin(np.pi*self.SENSOR_ANGLE_DEGREES/180)))
        if 3 in list_chgt :
            self.canevas.coords(self.turn_arrow, 350-self.TURN_SPEED, 550, 350, 595, 350+self.TURN_SPEED, 550)
        if 4 in list_chgt :
            self.canevas.coords(self.mv_arrow, 350-self.MOVE_SPEED, 10, 350+self.MOVE_SPEED, 10)
        if 5 in list_chgt:
            self.canevas.coords(self.lost_rect, 10, 400-200*self.LOST_SPEED, 30, 400)
            self.canevas.coords(self.cadre_lost_rect, 10, 200, 30, 400)
        if 8 in list_chgt:
            self.canevas.coords(self.home, 950-self.HOME_SIZE, 105-self.HOME_SIZE,950+self.HOME_SIZE, 105+self.HOME_SIZE)
            self.canevas.itemconfigure(self.txt_home,  font='Times '+str(int(self.HOME_SIZE/2))+' bold')
        if 9 in list_chgt:
            self.canevas.coords(self.food, 950-self.FOOD_SIZE, 310-self.FOOD_SIZE,950+self.FOOD_SIZE, 310+self.FOOD_SIZE)
            self.canevas.itemconfigure(self.txt_food,  font='Times '+str(int(self.FOOD_SIZE/2))+' bold')
        if 10 in list_chgt:
            self.display_foods()
        self.display_random()
        
        self.after(100, self.refresh)

    def display_random(self):
        """
        Affichage du disque à une place aléatoire dépendante de RANDOM_FACT
        Input, output : None
        """
        place = random.randint(-self.RANDOM_FACT, self.RANDOM_FACT)
        self.canevas.coords(self.oval_random, 1187+place*25, 500, 1212+place*25, 525)

    def display_foods(self):
        """
        Affichage de FOOD_COUNT disques représentants la nourriture disponible dans certains cas
        Input, output : None
        """
        for i in range(10):
            x = i%5
            y = i//5
            if i < self.FOOD_COUNT:
                self.canevas.itemconfigure(self.list_oval_foods[y][x], state='normal', fill=self.COLORS['food'])
            else:
                self.canevas.itemconfigure(self.list_oval_foods[y][x], state='hidden')

    def blink(self):
        """
        Affichage du clignotement de l'apparition des phéromones
        Input, output : None
        """
        if self.decay_dis :
            self.canevas.itemconfigure(self.decay_rect, state='hidden')
            self.decay_dis = False
        else : 
            self.canevas.itemconfigure(self.decay_rect, state='normal')
            self.decay_dis = True
        self.after(int(1000*self.DECAY_RATE), self.blink)

    def color(self, value):
        """
        Transformation d'une valeur comprise en 0 et 1 en teinte de gris en couleur hexadécimal
        Input : value, float correspondant à l'intensité de couleur voulue
        Output : color_hexa, sting couleur hexadécimal de la teinte de gris
        """
        color_hexa='#'
        value = int(value*128+127)
        value = min(value, 255)
        hexa = str(hex(value))[2:]
        if len(hexa)==1:
            hexa='0'+hexa
        color_hexa+=hexa*3

        return color_hexa

    def color_choice(self, event):
        color = colorchooser.askcolor(title="Choisissez une couleur")
        if color[1] is not None:
            return color[1]

    def change_color(self, event):
        id_change = self.canevas.find_withtag('current')[0]
        color = self.color_choice('<Button-1>')
        self.canevas.itemconfigure(id_change, fill=color)
        self.dico_color[id_change]['color']=color
        if 'pheromones' not in self.dico_color[id_change]['nom']:
            self.COLORS[self.dico_color[id_change]['nom']]=self.dico_color[id_change]['color']
            self.canevas.itemconfigure(self.home, fill=self.COLORS['maison'])
            self.canevas.itemconfigure(self.food, fill=self.COLORS['food'])
            self.display_foods()
        else:
            if '_0' in self.dico_color[id_change]['nom']:
                self.COLORS['pheromones'][0] = self.dico_color[id_change]['color']
                self.canevas.itemconfigure(self.decay_rect, fill=self.COLORS['pheromones'][0])
            else :
                self.COLORS['pheromones'][1] = self.dico_color[id_change]['color']       

    def spread_blink(self):
        """
        Calcul régulier (tous les SPREAT_RATE s) des intensités des phéromones se propageant
        Input, output : None
        """
        self.recover()
        i = self.spread_val
        self.area_spread_save = [[0 for i in range(9)] for j in range(9)]
        if i<5 and i>=0: 
            for y in range(1, 8):
                for x in range(1, 8):
                    if self.area_spread[y][x]!=0:
                        value_spread = self.area_spread[y][x]/2.5
                        self.area_spread_save[y][x]+=value_spread
                        self.area_spread_save[y][x-1]+=value_spread
                        self.area_spread_save[y][x+1]+=value_spread
                        self.area_spread_save[y-1][x]+=value_spread
                        self.area_spread_save[y+1][x]+=value_spread
            self.area_spread = self.area_spread_save
            self.spread_val+=1
        else:
            self.spread_val=0
            self.area_spread = [[0 for i in range(9)] for j in range(9)]
            self.area_spread[4][4] = 1
        self.display_spread()
        self.after(int(1000*self.SPREAD_RATE), self.spread_blink)

    def display_spread(self):
        """
        Affichage des phéromones se propageant en teinte de gris
        Input, output : None
        """
        for y in range(len(self.area_spread)):
            for x in range(len(self.area_spread[0])):
                self.canevas.itemconfigure(self.list_rect_spread[y][x], fill=self.color(self.area_spread[y][x]))

    def scroll(self, event):
        """
        Lancement du défilement du canevas et changement de paramètres modifiables
        Input, output : None (event ne nous sert pas mais la fonction est lancée par un bind)
        """
        self.xscroll(0)
        if self.gauche:
            self.canevas.pack_forget()
            self.left_zone.pack_forget()
            self.left_zone2.pack(side='left')
            self.canevas.pack(anchor='e')
            self.gauche=True
        else:
            self.canevas.pack_forget()
            self.left_zone2.pack_forget()
            self.left_zone.pack(side='left')
            self.canevas.pack(anchor='e')
            self.gauche=False

    def xscroll(self, i):
        """
        Défilement progressif en 100 étapes du canevas
        Input : i, integer nombre de l'étape de défilement
        Output : None
        """
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

    def end(self, event):
        """
        Dernière sauvegarde des paramètres et fermeture de la fenêtre
        Input, output : None
        """
        self.recover()
        self.quit()
        self.destroy()

    def parameter_save(self,event):
        name = self.texte.get()
        if name == "Nom de la configuration à enregistrer" or name == "":
            self.label_message.config(text = "Veuillez entrer un nom de configuration", fg='red')
            return
        
        if self.f_path == None:
            self.label_message.config(text = "Veuillez choisir un fichier", fg='red')
            return
        open('parametres_fourmis_(default).csv', 'a', newline='')
        liste_param = [name,self.val_sens_offset_dist.get(), self.val_sens_size.get(), self.val_sens_angle.get(), self.val_turn_spd.get(), self.val_mv_spd.get(), self.val_lost_spd.get(), self.val_decay_rate.get(), self.val_spread_rate.get(), self.val_home_size.get(), self.val_food_size.get(), self.val_food_count.get(), self.val_random_fact.get()]
        with open(self.f_path, 'a', newline='') as csvfile:
            
            writer = csv.writer(csvfile)
            writer.writerow(liste_param)
        self.label_message.config(text = "Configuration enregistrée", fg='green')
    
    def change_value(self, event):
        if self.f_path == None:
            self.label_message.config(text = "Veuillez choisir un fichier", fg='red')
            return

        with open(self.f_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            liste = []
            
            for row in reader:

                if row[0] == self.menu_deroulant.get():
                    liste = row

        self.val_sens_offset_dist.set(liste[1])
        self.val_sens_size.set(liste[2])
        self.val_sens_angle.set(liste[3])
        self.val_turn_spd.set(liste[4])
        self.val_mv_spd.set(liste[5])
        self.val_lost_spd.set(liste[6])
        self.val_decay_rate.set(liste[7])
        self.val_spread_rate.set(liste[8])
        self.val_home_size.set(liste[9])
        self.val_food_size.set(liste[10])
        self.val_food_count.set(liste[11])
        self.val_random_fact.set(liste[12])

    def supprimer_param(self,event):
        liste = self.menu_deroulant["values"]
        if len(liste) == 0:
            self.label_message.config(text = "Aucune configuration à supprimer", fg='red')
            return

        liste = list(liste)
        index = self.menu_deroulant.current()
        value = self.menu_deroulant.get().split(' ')


        liste.pop(index)
        self.menu_deroulant.config(values=liste)
        if len(liste) != 0:
            self.menu_deroulant.current(0)
        


        new_csv = []
        with open(self.f_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not ( row[0].split(' ') == value):
                    new_csv.append(row)
        with open(self.f_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in new_csv:
                writer.writerow(row)

        return value,index

    def verr_param(self,event):
        f = open("constants.py", "r")
        lines = f.readlines()
        f.close()
        
        f = open("constants.py", "w")
        
        for line in lines:
            if "SENSOR_OFFSET_DISTANCE" in line:
                f.write(f'SENSOR_OFFSET_DISTANCE: int = {self.SENSOR_OFFSET_DISTANCE}\n')
            elif "SENSOR_SIZE" in line:
                f.write(f'SENSOR_SIZE: int = {self.SENSOR_SIZE}\n')
            elif "SENSOR_ANGLE_RAD" in line:
                f.write(f'SENSOR_ANGLE_RAD: float = {self.SENSOR_ANGLE_DEGREES} * 3.14 / 180\n')
            elif "TURN_SPEED" in line:
                f.write(f'TURN_SPEED: float = {self.TURN_SPEED}  * 3.14 / 180\n')
            elif "MOVE_SPEED" in line:
                f.write(f'MOVE_SPEED: int = {self.MOVE_SPEED}\n')
            elif "RANDOM_FACT" in line:
                f.write(f'RANDOM_FACT: int = {self.RANDOM_FACT}\n')
        
            elif "DECAY_RATE" in line:
                f.write(f'DECAY_RATE: float = {self.DECAY_RATE}\n')
            elif "SPREAD_RATE" in line:
                f.write(f'SPREAD_RATE: float = {self.SPREAD_RATE}\n')
            elif "HOME_SIZE" in line:
                f.write(f'HOME_SIZE: int = {self.HOME_SIZE}\n')
            elif "FOOD_SIZE" in line:
                f.write(f'FOOD_SIZE: int = {self.FOOD_SIZE}\n')
            elif "FOOD_COUNT" in line:
                f.write(f'FOOD_COUNT: int = {self.FOOD_COUNT}\n')
            elif "LOST_SPEED" in line:
                f.write(f'LOST_SPEED: float = {self.LOST_SPEED}\n')
            elif "colors" in line:
                f.write(f'colors = {self.COLORS}\n')
            else:
                f.write(line)

        f.close()
         
        c.SENSOR_OFFSET_DISTANCE = self.SENSOR_OFFSET_DISTANCE
        c.SENSOR_SIZE = self.SENSOR_SIZE
        c.SENSOR_ANGLE_RAD = self.SENSOR_ANGLE_DEGREES * 3.14 / 180
        c.TURN_SPEED = self.TURN_SPEED
        c.MOVE_SPEED = self.MOVE_SPEED
         
        self.end(event)

    def chose_file(self,event):
        self.f_path = askopenfilename(initialdir="./",title="Select File", filetypes=(("CSV files","*.csv*"),("All Files","*.*")))
        if self.f_path == "":
            self.label_message.config(text = "Veuillez choisir un fichier", fg='red')
            self.f_path = None
            return
        self.label_message.config(text = "Fichier choisi", fg='green')
        self.refresh_menu_deroulant(event)

    def refresh_menu_deroulant(self,event):
        if self.f_path == None:
            self.label_message.config(text = "Veuillez choisir un fichier", fg='red')
            return
        with open(self.f_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            liste = []
            for row in reader:
                liste.append(row[0])
        self.menu_deroulant.config(values=liste)
        if len(liste) != 0:
            self.menu_deroulant.current(0)

class Color_choice(tk.Tk):

    def __init__(self):
        pass


if __name__ == "__main__":
    app = Display_set()
    app.mainloop() 