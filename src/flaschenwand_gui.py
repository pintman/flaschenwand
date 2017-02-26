import tkinter

class FlaschenwandGui:
    def __init__(self, width=6, height=4):
        self.width = width
        self.height = height
        self.coords_rect = dict()

        self.root = tkinter.Tk()

        width_px = 600
        height_px = 400
        self.canvas = tkinter.Canvas(self.root, width=width_px, height=height_px)
        for x in range(width):
            for y in range(height):
                width_per_pixel = width_px/width
                height_per_pixel = height_px/height
                self.coords_rect[(x,y)] = self.canvas.create_rectangle(
                    x * width_per_pixel,
                    y * height_per_pixel,
                    x * width_per_pixel + width_per_pixel,
                    y * height_per_pixel + height_per_pixel,
                    fill="#000000")
        self.canvas.pack()

        self.update()
        self.root.mainloop()

    def set_pixel_rgb(self, x, y, r, g, b):
        tk_rgb = "#%02x%02x%02x" % (r, g, b)
        self.canvas.itemconfig(self.coords_rect[(x,y)], fill=tk_rgb)

    def update(self):
        # plasma demo
        import time, math, colorsys
        current = time.time()

        for x in range(self.width):
            for y in range(self.height):
                v = math.sin(x*25.0 + current)
                # -1 < sin() < +1
                # therfore correct the value and bring into range [0, 1]
                v = (v+1.0) / 2.0
                # transform from hsv to rgb: cycle through colors.
                r, g, b = colorsys.hsv_to_rgb(v, 1, v)
                self.set_pixel_rgb(x, y, int(r*255), int(g*255), int(b*255))

        self.root.after(10, self.update)

def main():
    gui = FlaschenwandGui()

if __name__ == "__main__":
    main()
