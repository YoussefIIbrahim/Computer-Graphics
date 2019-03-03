import os
import tkinter
from tkinter import filedialog

import PIL.Image
import PIL.ImageTk
import cv2

from Filters import filters
from Filters import graph_filters


class App:
    def __init__(self, root, root_title, image_path="init.png"):
        self.root = root
        self.root.title(root_title)
        self.path = None
        self.image = None
        self.first_filter = 0
        menu = tkinter.Menu()
        self.root.config(menu=menu)

        file = tkinter.Menu(menu, tearoff=0)
        file.add_command(label='Open Image...', command=self.open_image)
        file.add_command(label='Open Graph', command=self.open_graph)
        file.add_command(label='Reset', command=self.reset_image)
        menu.add_cascade(label="File", menu=file)

        self.topFrame = tkinter.Frame()
        self.topFrame.pack()

        # Load an image using OpenCV
        self.cv_img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_img.shape

        # Create a canvas that can fit the above image
        self.canvasOne = tkinter.Canvas(self.topFrame, width = self.width, height = self.height)
        self.canvasOne.pack(expand=True, side=tkinter.LEFT)

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photoOne = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))

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

        # Button for inversion
        self.btn_inversion = tkinter.Button(self.bottomFrame, text="Inversion", width=50, command= self.invert_image)
        self.btn_inversion.grid(row=0, column=0)

        # Button for brightness
        self.btn_bright = tkinter.Button(self.bottomFrame, text="Brightness Correction", width=50, command=self.brightness)
        self.btn_bright.grid(row=0, column=1)

        # Button for contrast
        self.btn_contrast = tkinter.Button(self.bottomFrame, text="Contrast Enhancement", width=50, command=self.contrast)
        self.btn_contrast.grid(row=0, column=2)

        # Button for gamma
        self.btn_gamma = tkinter.Button(self.bottomFrame, text="Gamma Correction", width=50, command=self.gamma)
        self.btn_gamma.grid(row=1, column=0)

        # Button for blur
        self.btn_blur = tkinter.Button(self.bottomFrame, text="Blur 3x3", width=50, command=self.blur_image)
        self.btn_blur.grid(row=1, column=1)

        # Gaussian
        self.btn_gaussian = tkinter.Button(self.bottomFrame, text="Gaussian Smoothing 3x3", width=50, command=self.gaussian_blur)
        self.btn_gaussian.grid(row=1, column=2)

        # Sharpen
        self.btn_sharpen = tkinter.Button(self.bottomFrame, text="Sharpen 3x3", width=50, command=self.sharpen)
        self.btn_sharpen.grid(row=2, column=0)

        # Edge Detection
        self.btn_edge_detection = tkinter.Button(self.bottomFrame, text="Edge Detection 3x3", width=50, command=self.edge_detection)
        self.btn_edge_detection.grid(row=2, column=1)

        # Emboss
        self.btn_emboss = tkinter.Button(self.bottomFrame, text="Emboss 3x3", width=50, command=self.emboss)
        self.btn_emboss.grid(row=2, column=2)

        self.root.mainloop()

    # Reset Image
    def reset_image(self):
        self.image = PIL.Image.open(self.path)
        self.canvas.create_image(0, 0, image=self.photoOne, anchor=tkinter.NW)
        # graph_filters.SecondApp(tkinter.Toplevel(), "Tkinter", self.path)

    # Reset Image
    def open_graph(self):
        graph_filters.SecondApp(tkinter.Toplevel(), "Tkinter", self.image, self.path)

    # Open File
    def open_image(self):
        self.path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Open image',
                                             filetypes=[('Image files', ('.png', '.jpg', '.bmp'))])
        self.image = PIL.Image.open(self.path)
        self.width, self.height = self.image.size
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.photoOne = PIL.ImageTk.PhotoImage(self.image)
        self.canvasOne.create_image(0, 0, image=self.photoOne, anchor=tkinter.NW)
        self.canvasOne.config(width=self.width, height=self.height)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.canvas.config(width=self.width, height=self.height)

    # Callback for the "Blur" button
    def invert_image(self):
        self.image = filters.inversion(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def brightness(self):
        self.image = filters.brightness_correction(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def contrast(self):
        self.image = filters.contrast_enhancement(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def blur_image(self):
        self.image = filters.blur(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def gamma(self):
        self.image = filters.gamma_correction(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def gaussian_blur(self):
        self.image = filters.gaussian(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def sharpen(self):
        self.image = filters.sharpen(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def edge_detection(self):
        self.image = filters.edge(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def emboss(self):
        self.image = filters.emboss(self.image)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


# Create a root and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
