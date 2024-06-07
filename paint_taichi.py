import taichi as ti

@ti.data_oriented
class Paint() :
    def __init__(self, width, height):
        self.size = ti.Vector([width, height])
        self.image = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))
        self.window = ti.GUI("Paint", (width, height))
        self.brush_size = self.window.slider("Brush size", 1, 50, 10)
        self.prev_pos = ti.Vector([0.0, 0.0])
        self.save = self.window.button("Save")

    def run(self) :
        mouse = ti.Vector([0.0, 0.0])
        while self.window.running :
            self.window.set_image(self.image)
            self.window.get_event()
            
            if self.window.is_pressed(ti.ui.LMB):
                mouse = ti.Vector(self.window.get_cursor_pos()) * self.size
                self.paint(mouse, False)
            elif self.window.is_pressed(ti.ui.RMB) :
                mouse = ti.Vector(self.window.get_cursor_pos()) * self.size
                self.paint(mouse, True)
            elif self.window.is_pressed(self.save) :
                ti.tools.imwrite(self.image, "./saved_images/paint.png")
            else :
                mouse = ti.Vector([0.0, 0.0])

            self.window.show()
            self.prev_pos = mouse
            ti.sync()

    @ti.kernel
    def paint(self, pos: ti.template(), erase: bool) :
        if self.prev_pos.norm() > 1.0 :
            vect_diff = pos - self.prev_pos
            for i in range(int(ti.round(vect_diff.norm()))) :
                self.fill_circle(ti.cast(self.prev_pos + vect_diff.normalized() * i, ti.i32), erase)
        
    @ti.func
    def fill_circle(self, pos: ti.template(), erase: bool) :
        size = ti.cast(self.brush_size.value, ti.i32)
        if erase :
            size = ti.cast(self.brush_size.value * 2, ti.i32)
        for i in range(-size, size) :
            for j in range(-size, size) :
                if ti.Vector([i, j]).norm() <= self.brush_size.value :
                    if self.is_in_window(pos + (i,j)) :
                        col = ti.Vector([0.0, 1.0, 0.0])

                        if erase :
                            col = ti.Vector([0.0, 0.0, 0.0])
                        self.image[pos + (i, j)] = col

    @ti.func
    def is_in_window(self, vect: ti.template()) :
        return vect[0] >= 0 and vect[0] < self.size[0] and vect[1] >= 0 and vect[1] < self.size[1]

if __name__ == "__main__" :
    ti.init(arch=ti.vulkan)
    Paint(512, 512).run()