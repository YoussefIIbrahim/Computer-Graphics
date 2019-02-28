import tkinter as tk

import matplotlib.backends.tkagg as tkagg
import matplotlib.pyplot as pypl
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.

    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w / 2, loc[1] + figure_h / 2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo


def callback(event):
    print("clicked at", event.x, event.y)
    canvas.create_oval((event.x) - 0.8, (event.y) - 0.8, (event.x) + 0.8, (event.y) + 0.8, outline="#f11",
                       fill="#1f1", width=2)


# Create a canvas
w, h = 250, 250
window = tk.Tk()
window.title("A figure in a canvas")

canvas = tk.Canvas(window, width=w, height=h)
canvas.bind("<Button-1>", callback)
canvas.pack()

# Generate some example data
X = np.linspace(0, 2.0 * 3.14, 50)
Y = X

# Create the figure we desire to add to an existing canvas
fig = pypl.figure(figsize=(2.50, 2.50), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.plot(X, Y)

# Keep this handle alive, or else figure will disappear
fig_x, fig_y = 0, 0
fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
fig_w, fig_h = fig_photo.width(), fig_photo.height()

# Add more elements to the canvas, potentially on top of the figure


# Let Tk take over
tk.mainloop()
