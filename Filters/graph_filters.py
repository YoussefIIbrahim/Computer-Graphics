import tkinter
from tkinter import messagebox

import PIL.Image
import PIL.ImageTk
import cv2
import matplotlib.backends.tkagg as tkagg
import matplotlib.pyplot as pypl
from matplotlib.backends.backend_agg import FigureCanvasAgg


class App:
    def __init__(self, window, window_title, image_path="init.png"):
        self.window = window
        self.window.title(window_title)
        self.path = None
        self.image = None
        self.Xes = []
        self.Yes = []
        self.eventX = []
        self.eventY = []
        self.first_filter = 0
        self.dragged = 0
        self.toleranceY = [-0.955, 321.854]
        self.toleranceX = [0.47398, -58.773]
        menu = tkinter.Menu()
        self.window.config(menu=menu)

        file = tkinter.Menu(menu, tearoff=0)
        file.add_command(label='Open Image...', command=self.draw_figure)
        menu.add_cascade(label="File", menu=file)

        self.topFrame = tkinter.Frame()
        self.topFrame.pack()

        # Load an image using OpenCV
        self.cv_img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_img.shape

        # Create a canvas that can fit the above image
        self.canvasOne = tkinter.Canvas(self.topFrame, width=self.width, height=self.height)
        self.canvasOne.pack(expand=True, side=tkinter.LEFT)

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photoOne = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))

        # Add a PhotoImage to the Canvas
        self.canvasOne.create_image(0, 0, image=self.photoOne, anchor=tkinter.NW)

        # Create a canvas that can fit the edited image
        self.canvas = tkinter.Canvas(self.topFrame, width=self.width, height=self.height)
        self.canvas.pack(expand=True, side=tkinter.LEFT)

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))
        #
        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.bottomFrame = tkinter.Frame()
        self.bottomFrame.pack()

        # Create a canvas
        w, h = 255 * 3, 255 * 1.5
        self.bottom_canvas = tkinter.Canvas(self.bottomFrame, relief=tkinter.RIDGE, width=w, height=h)
        self.bottom_canvas.bind("<Double-Button-1>", self.reconstruct_line)
        self.bottom_canvas.configure(background='black')
        self.bottom_canvas.tag_bind("DnD", "<ButtonPress-1>", self.down)
        self.bottom_canvas.tag_bind("DnD", "<ButtonRelease-1>", self.chkup)
        self.bottom_canvas.tag_bind("DnD", "<Enter>", self.enter)
        self.bottom_canvas.tag_bind("DnD", "<Leave>", self.leave)
        self.bottom_canvas.pack()

        # Generate some example data
        self.Xes = [[0, 0], [255, 255]]
        self.Yes = [0, 255]

        # # Create the figure we desire to add to an existing canvas
        # self.fig = pypl.figure(figsize=(8, 4), dpi=100)
        # self.ax = self.fig.add_subplot(1, 1, 1)
        # self.ax.plot(self.Xes, self.Yes)
        #
        # # Keep this handle alive, or else figure will disappear
        # fig_x, fig_y = 5, 5
        # fig_photo = self.draw_figure(self.bottom_canvas, self.fig, loc=(fig_x, fig_y))
        xes = [i[0] for i in self.Xes]
        yes = [i[1] for i in self.Xes]
        self.fig_photo = self.draw_figure(xes, yes)
        self.window.mainloop()

    # Draw the graoh using matplotlib
    def draw_figure(self, x_values, y_values):
        pypl.close()
        # Create the figure we desire to add to an existing canvas
        fig = pypl.figure(figsize=(2.55 * 3, 2.55 * 1.5), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.clear()
        ax.plot(x_values, y_values)

        # Keep this handle alive, or else figure will disappear
        fig_x, fig_y = 0, 0

        # fig.canvas.draw()

        figure_canvas_agg = FigureCanvasAgg(fig)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tkinter.PhotoImage(master=self.bottom_canvas, width=figure_w, height=figure_h)

        # Position: convert from top-left anchor to center anchor
        self.bottom_canvas.create_image(fig_x + figure_w / 2, fig_y + figure_h / 2 + 10, image=photo)
        for i in range(len(self.eventX)):
            self.bottom_canvas.create_oval((self.eventX[i]) - 5, (self.eventY[i]) - 5, (self.eventX[i]) + 5,
                                           (self.eventY[i]) + 5,
                                           outline="#f11", fill="#1f1", width=2, tags="DnD")
        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo

    # Reconstruct the drawn line on marker drop
    def reconstruct_line(self, event):
        x = int(((event.x) * self.toleranceX[0]) + self.toleranceX[1])
        y = int(((event.y) * self.toleranceY[0]) + self.toleranceY[1])

        if 0 <= x <= 255 and 0 <= y <= 255:
            self.eventX.append(event.x)
            self.eventY.append(event.y)
            self.Xes.append([x, y])
            self.fig_photo = self.draw_figure([i[0] for i in self.Xes], [i[1] for i in self.Xes])

    # Drag points
    def down(self, event):
        self.loc = 1
        self.dragged = 0
        event.widget.bind("<Motion>", self.motion)
        x_mod = int((event.x * self.toleranceX[0]) + self.toleranceX[1])
        y_mod = int((event.y * self.toleranceY[0]) + self.toleranceY[1])
        print(self.Xes)
        print(self.Yes)
        print(self.eventX)
        print(self.eventY)
        self.RemoveXesYes(x_mod, y_mod)


    def motion(self, event):
        self.window.config(cursor="exchange")
        cnv = event.widget
        cnv.itemconfigure(tkinter.CURRENT, fill="blue")
        x, y = cnv.canvasx(event.x), cnv.canvasy(event.y)
        x_modified = int((x * self.toleranceX[0]) + self.toleranceX[1])
        y_modified = int((y * self.toleranceY[0]) + self.toleranceY[1])
        if 255 >= x_modified >= 0 and 255 >= y_modified >= 0:
            got = event.widget.coords(tkinter.CURRENT, x - 10, y - 10, x + 10, y + 10)
            # self.Xes.append(x)
            # self.Yes.append(y)
            # self.Xes.sort()
            # self.Yes.sort()
            # self.fig_photo = self.draw_figure(self.Xes, self.Yes)

    def leave(self, event):
        self.loc = 0

    def enter(self, event):
        self.loc = 1
        if self.dragged == event.time:
            self.up(event)

    def chkup(self, event):
        event.widget.unbind("<Motion>")
        self.window.config(cursor="")
        self.target = event.widget.find_withtag(tkinter.CURRENT)
        event.widget.itemconfigure(tkinter.CURRENT)
        x_mod = int((event.x * self.toleranceX[0]) + self.toleranceX[1])
        y_mod = int((event.y * self.toleranceY[0]) + self.toleranceY[1])
        if x_mod > 255:
            x_mod = 255
        if y_mod > 255:
            y_mod = 255
        if x_mod < 0:
            x_mod = 0
        if y_mod < 0:
            y_mod = 0
        self.addXesYes(x_mod, y_mod)
        self.fig_photo = self.draw_figure([i[0] for i in self.Xes], [i[1] for i in self.Xes])

        if self.loc:  # is button released in same widget as pressed?
            self.up(event)


        else:
            self.dragged = event.time

    def up(self, event):
        event.widget.unbind("<Motion>")
        if (self.target == event.widget.find_withtag(tkinter.CURRENT)):
            print("Select %s" % event.widget)
        else:
            event.widget.itemconfigure(tkinter.CURRENT, fill="blue")
            self.window.update()

    def RemoveXesYes(self, x_mod, y_mod):
        x_remove = x_mod
        y_remove = y_mod
        x_event = int((x_mod - self.toleranceX[1]) / self.toleranceX[0])
        y_event = int((y_mod - self.toleranceY[1]) / self.toleranceY[0])

        # Handlling margin or error for Event Click by one or two steps
        for i in range(-10, 10):
            for k in range(-10, 10):
                if x_event + i in self.eventX and y_event + k in self.eventY:
                    x_event = x_event + i
                    y_event = y_event + k

        for i in range(len(self.Xes)):
            pass
        # Handling margin error for saved points
        for i in range(-10, 10):
            for k in range(-10, 10):
                if x_remove + i in self.Xes and y_remove + k in self.Yes:
                    x_remove = x_remove + i
                    y_remove = y_remove + k

        # Handling not finding the points
        if x_remove not in self.Xes or y_remove not in self.Yes or x_event not in self.eventX or y_event not in self.eventY:

            messagebox.showinfo("Error", "Error retrieving this point from set of points. Please try again.")
        else:
            print("Yes remove", y_event, self.eventY)
            print("Yes remove", x_event, self.eventX)
            print("Yes remove", y_remove, self.Yes)
            print("Yes remove", x_remove, self.Xes)
            self.Xes.remove(x_remove)
            self.Yes.remove(y_remove)
            self.eventX.remove(x_event)
            self.eventY.remove(y_event)

    def addXesYes(self, x_mod, y_mod):

        self.eventX.append(int((x_mod - self.toleranceX[1]) / self.toleranceX[0]))
        self.eventY.append(int((y_mod - self.toleranceY[1]) / self.toleranceY[0]))
        self.Xes.append(x_mod)
        self.Yes.append(y_mod)

        self.Xes.sort()
        self.Yes.sort()

App(tkinter.Tk(), "Tkinter and OpenCV")
