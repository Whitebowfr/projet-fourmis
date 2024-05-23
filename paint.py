from tkinter import filedialog, messagebox
from tkinter import *
from tkinter.colorchooser import askcolor
import taichi as ti
import os
from PIL import Image, ImageTk
import io

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'green'

    def __init__(self, width, height):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=1)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)

        self.choose_size_button = Scale(self.root, from_=1, to=50, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=3)

        self.upload_button = Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=0, column=4)

        self.save_button = Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.grid(row=0, column=5)

        self.c = Canvas(self.root, bg='white', width=width, height=height)
        self.c.grid(row=2, columnspan=6)
        self.c.create_rectangle(0, 0, width+100, height+100, fill="black")

        self.setup()
        self.root.mainloop()

        prebuilt = ti.tools.imread("./saved_images/output.png")
        prebuilt = ti.tools.imresize(prebuilt, width, height)
        print(type(prebuilt))

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'black' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((300, 300))  # Resize image if necessary
            self.photo = ImageTk.PhotoImage(self.image)
            self.c.create_image(0, 0, image=self.photo, anchor=NW)
            messagebox.showinfo("Success", "Image uploaded successfully!")

    def save_image(self):
        save_dir = "saved_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        #file_path = filedialog.asksaveasfilename(defaultextension=".png")
        #filename = os.path.basename(file_path)
        postscript_file = self.c.postscript(colormode='color')
        image = Image.open(io.BytesIO(postscript_file.encode('utf-8')))
        image.save('./saved_images/output.png')

        print("Image saved to: ./saved_images/output.png")


if __name__ == '__main__':
    paint = Paint(700, 700)

