import tkinter

from Rasterization.Circle import Circle
from Rasterization.CopyingPixels import copyingPixels
from Rasterization.Line import Line


class App:
    def __init__(self, root, root_title):
        self.root = root
        self.root.title(root_title)

        menu = tkinter.Menu()
        self.root.config(menu=menu)

        operations = tkinter.Menu(menu, tearoff=0)

        operations.add_command(label='Line', command=lambda: self.open_line())
        operations.add_command(label='Thick Line', command=lambda: self.open_brush())
        operations.add_command(label='Circle', command=lambda: self.open_circle())

        menu.add_cascade(label='Draw', menu=operations)

        file = tkinter.Menu(menu, tearoff=0)
        file.add_command(label='Clear canvas', command=self.reset)
        menu.add_cascade(label='File', menu=file)

        self.canvas = tkinter.Canvas(self.root, width=500, height=500)
        self.canvas.configure(bg='white')
        self.canvas.pack()
        self.root.mainloop()

    def open_line(self):
        Line(self)

    def open_brush(self):
        copyingPixels(self)

    def open_circle(self):
        Circle(self)

    def draw_pixel(self, x, y):
        self.canvas.create_line(x + 2, y + 2, x + 3, y + 2, fill="#%02x%02x%02x" % ((0,) * 3))

    def draw_pixels(self, pixels):
        for pixel in pixels:
            self.draw_pixel(pixel[0], pixel[1])

    def draw_line(self, x1, y1, x2, y2):
        if x2 < x1: x1, x2 = x2, x1
        if y2 < y1: y1, y2 = y2, y1
        pixels = []
        if y1 == 0: y1 = 1
        if y2 == 0: y2 = 1
        dy = y2 - y1
        dx = x2 - x1
        m = (dy / dx) if (dx != 0) else (dx / dy)
        y = y1
        x = x1
        length = (x2 - x1) if (x2 - x1) > (y2 - y1) else (y2 - y1)
        length = abs(length)
        for i in range(length):
            if dx != 0:
                pixels.append((i, round(y)))
                y += m
            else:
                pixels.append((round(x), i))
                x += m
        print(pixels)
        self.draw_pixels(pixels)

    def draw_circle(self, x, y, r):

        pixels = []
        dE = 3
        dSE = 5 - 2 * r
        d = 1 - r
        xx = 0
        yy = r
        pixels.extend(self.getCircumPixels(x, y, xx, yy))

        while yy > xx:
            if d < 0:
                d += dE
                dE += 2
                dSE += 2
            else:
                d += dSE
                dE += 2
                dSE += 4
                yy -= 1
            xx += 1
            pixels.extend(self.getCircumPixels(x, y, xx, yy))

        self.draw_pixels(pixels)

    def getCircumPixels(self, x, y, dx, dy):
        return [
            (x + dx, y + dy, 0),
            (x - dx, y + dy, 0),
            (x + dx, y - dy, 0),
            (x - dx, y - dy, 0),
            (x + dy, y + dx, 0),
            (x - dy, y + dx, 0),
            (x + dy, y - dx, 0),
            (x - dy, y - dx, 0)
        ]

    def drawThickLine(self, x1, y1, x2, y2, thick):
        pixels = []
        if y1 == 0: y1 = 1
        if y2 == 0: y2 = 1
        dy = y2 - y1
        dx = x2 - x1
        m = (dy / dx) if (dx != 0) else (dx / dy)
        y = y1
        x = x1
        length = (x2 - x1) if (x2 - x1) > (y2 - y1) else (y2 - y1)
        length = abs(length)
        for i in range(length):
            if dx != 0:
                pixels.append((i, round(y)))
                y += m
            else:
                pixels.append((round(x), i))
                x += m

        new_pixels = []
        for pixel in pixels:
            for i in range(thick * 2 - 1):
                for j in range(thick * 2 - 1):
                    new_pixels.append((
                        pixel[0] - thick + 1 + i,
                        pixel[1] - thick + 1 + j
                    ))
        self.draw_pixels(new_pixels)

    def reset(self):
        self.canvas.delete("all")


App(tkinter.Tk(), "Tkinter and OpenCV for Task 3")
