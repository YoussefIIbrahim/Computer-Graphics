import tkinter

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
        self.first_filter = 0
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
        w, h = 800, 400
        self.bottom_canvas = tkinter.Canvas(self.bottomFrame, width=w, height=h)
        self.bottom_canvas.bind("<Button-1>", self.reconstruct_line)
        self.bottom_canvas.pack()

        # Generate some example data
        self.Xes = [0, 255]
        self.Yes = [0, 255]

        # # Create the figure we desire to add to an existing canvas
        # self.fig = pypl.figure(figsize=(8, 4), dpi=100)
        # self.ax = self.fig.add_subplot(1, 1, 1)
        # self.ax.plot(self.Xes, self.Yes)
        #
        # # Keep this handle alive, or else figure will disappear
        # fig_x, fig_y = 5, 5
        # fig_photo = self.draw_figure(self.bottom_canvas, self.fig, loc=(fig_x, fig_y))
        self.fig_photo = self.draw_figure(self.Xes, self.Yes)
        self.window.mainloop()

    # Draw the graoh using matplotlib
    def draw_figure(self, x_values, y_values):
        # Create the figure we desire to add to an existing canvas
        fig = pypl.figure(figsize=(2.55 * 3, 2.55 * 1.5), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.clear()
        print("Here")
        ax.plot(x_values, y_values)
        print(id(ax))

        # Keep this handle alive, or else figure will disappear
        fig_x, fig_y = 5, 5

        # fig.canvas.draw()

        figure_canvas_agg = FigureCanvasAgg(fig)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tkinter.PhotoImage(master=self.bottom_canvas, width=figure_w, height=figure_h)

        # Position: convert from top-left anchor to center anchor
        self.bottom_canvas.create_image(fig_x + figure_w / 2, fig_y + figure_h / 2, image=photo)
        for i in range(len(self.Xes)):
            self.bottom_canvas.create_oval((self.Xes[i]) - 0.8, (self.Yes[i]) - 0.8, (self.Xes[i]) + 0.8,
                                           (self.Yes[i]) + 0.8,
                                           outline="#f11", fill="#1f1", width=2)
        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo

    # Reconstruct the drawn line on marker drop
    def reconstruct_line(self, event):
        self.bottom_canvas.create_oval((event.x) - 0.8, (event.y) - 0.8, (event.x) + 0.8, (event.y) + 0.8,
                                       outline="#f11",
                                       fill="#1f1", width=2)
        self.Xes.append(event.x / 3)
        self.Yes.append(event.y / 1.5)
        self.Xes.sort()
        self.Yes.sort()
        print(self.Xes, self.Yes)
        self.fig_photo = self.draw_figure(self.Xes, self.Yes)


# # Create a canvas
# w, h = 800, 500
# window = tk.Tk()
# window.title("A figure in a canvas")
#
# canvas = tk.Canvas(window, width=w, height=h)
# canvas.bind("<Button-1>", reconstruct_line)
# canvas.pack()
#
# # Generate some example data
# X = [0, 255]
# Y = X
#
# # Create the figure we desire to add to an existing canvas
# fig = pypl.figure(figsize=(8, 5), dpi=100)
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(X, Y)
#
# # Keep this handle alive, or else figure will disappear
# fig_x, fig_y = 10, 10
# fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
# fig_w, fig_h = fig_photo.width(), fig_photo.height()
#
# # Add more elements to the canvas and reconstruct graph
#
#
#
# # Let Tk take over
# tk.mainloop()
App(tkinter.Tk(), "Tkinter and OpenCV")
