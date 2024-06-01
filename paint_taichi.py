import taichi as ti

ti.init(arch=ti.vulkan)

coordinates_type = ti.types.vector(2, ti.f32)

@ti.data_oriented
class Paint() :
    def __init__(self, width, height):
        self.size = ti.Vector([width, height])
        self.image = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))
        self.window = ti.ui.Window("Paint", (width, height))
        self.canvas = self.window.get_canvas()
        self.gui = self.window.get_gui()
        self.brush_size = 5
        self.brush_type = "Food"
        self.prev_pos = ti.Vector([0.0, 0.0])
        self.run()

    def run(self) :
        while self.window.running :
            mouse = ti.Vector(self.window.get_cursor_pos()) * self.size
            if self.window.is_pressed(ti.ui.LMB) :
                self.paint(mouse, False)
            elif self.window.is_pressed(ti.ui.RMB) :
                self.paint(mouse, True)
                
            with self.gui.sub_window("Paramètres", 0.05, 0.05, 0.5, 0.35) :
                self.gui.text("Type : " + self.brush_type)
                if self.gui.button("Food") :
                    self.brush_type = "Food"
                if self.gui.button("Home") :
                    self.brush_type = "Home"
                if self.gui.button("Obstacle") :
                    self.brush_type = "Obstacle"
                self.brush_size = self.gui.slider_float("Taille", self.brush_size, 1, 20)
                if self.gui.button("Save") :
                    ti.tools.imwrite(self.image, "./saved_images/paint.png")

            self.canvas.set_image(self.image)
            self.window.show()
            self.prev_pos = mouse

    @ti.kernel
    def paint(self, pos: coordinates_type, erase: bool) :
        if self.prev_pos.norm() > 0 :
            vect_diff = pos - self.prev_pos
            for i in range(ti.round(vect_diff.norm())) :
                print(i)
                self.fill_circle(self.prev_pos + vect_diff.normalized() * i, erase)
        
    @ti.func
    def fill_circle(self, pos: coordinates_type, erase: bool) :
        center = ti.cast(pos, ti.i32)
        size = ti.cast(self.brush_size, ti.i32)
        if erase :
            size = ti.cast(self.brush_size * 2, ti.i32)
        for i in range(-size, size) :
            for j in range(-size, size) :
                if ti.Vector([i, j]).norm() <= self.brush_size :
                    col = ti.Vector([0.0, 0.0, 0.0])
                    if self.brush_type == "Food" :
                        col = ti.Vector([0.0, 1.0, 0.0])
                    elif self.brush_type == "Home" :
                        col = ti.Vector([0.0, 0.0, 1.0])
                    elif self.brush_type == "Obstacle" :
                        col = ti.Vector([0.1, 0.1, 0.1])

                    if erase :
                        col = ti.Vector([0.0, 0.0, 0.0])
                    self.image[center + (i, j)] = col

if __name__ == "__main__" :
    Paint(512, 512)