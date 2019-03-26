import os
import tkinter
from tkinter import filedialog

import PIL.Image
import PIL.ImageTk
import cv2

from ErrorDiffusionUniformQuantization import filters
from ErrorDiffusionUniformQuantization import uniformQunatization


class App:
    def __init__(self, root, root_title, image_path="init.png"):
        self.root = root
        self.root.title(root_title)
        self.path = None
        self.image = None
        self.var = None
        self.first_filter = 0
        menu = tkinter.Menu()
        self.root.config(menu=menu)

        file = tkinter.Menu(menu, tearoff=0)
        file.add_command(label='Open Image...', command=self.open_image)
        file.add_command(label='Reset', command=self.reset_image)
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

        self.var = tkinter.IntVar()
        self.var.set(2)
        R1 = tkinter.Radiobutton(self.bottomFrame, text="M equals 2", variable=self.var, value=2)
        R2 = tkinter.Radiobutton(self.bottomFrame, text="M equals 4", variable=self.var, value=4)
        R3 = tkinter.Radiobutton(self.bottomFrame, text="M equals 8", variable=self.var, value=8)
        R4 = tkinter.Radiobutton(self.bottomFrame, text="M equals 16", variable=self.var, value=16)
        R1.grid(row=0, column=0)
        R2.grid(row=0, column=1)
        R3.grid(row=0, column=2)
        R4.grid(row=0, column=3)

        # Button for floyd-steinberg
        self.btn_inversion = tkinter.Button(self.bottomFrame, text="Floyd and Steinberg Filter", width=50,
                                            command=self.steinberg)
        self.btn_inversion.grid(row=1, column=0, columnspan=2)

        # Button for Burkes
        self.btn_bright = tkinter.Button(self.bottomFrame, text="Burkes Filter", width=50,
                                         command=self.burkes)
        self.btn_bright.grid(row=1, column=2, columnspan=2)

        # Button for Stucky
        self.btn_contrast = tkinter.Button(self.bottomFrame, text="Stucky Filter", width=50,
                                           command=self.stucky)
        self.btn_contrast.grid(row=2, column=0, columnspan=2)

        # Button for Sierra
        self.btn_gamma = tkinter.Button(self.bottomFrame, text="Sierra Filter", width=50, command=self.sierra)
        self.btn_gamma.grid(row=2, column=2, columnspan=2)

        # Button for Atkinson
        self.btn_blur = tkinter.Button(self.bottomFrame, text="Atkinson Filter", width=50, command=self.atkinson)
        self.btn_blur.grid(row=3, columnspan=4)

        # Slider for Num Colors
        self.slider = tkinter.Scale(self.bottomFrame, from_=2, to=256, length=self.width, orient=tkinter.HORIZONTAL)
        self.slider.grid(row=4, columnspan=4)

        # Button for UniformQuantization
        self.btn_quant = tkinter.Button(self.bottomFrame, text="Uniform Quantization", width=50,
                                        command=self.uniformQuantization)
        self.btn_quant.grid(row=5, columnspan=4)

        self.root.mainloop()

    # Reset Image
    def reset_image(self):
        self.image = PIL.Image.open(self.path)
        self.canvas.create_image(0, 0, image=self.photoOne, anchor=tkinter.NW)
        # graph_filters.SecondApp(tkinter.Toplevel(), "Tkinter", self.path)

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

    # Callback for the steinberg button
    def steinberg(self):
        self.image = filters.useFilter(self.image, self.var.get(), 'floyd-steinberg')
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the burkes button
    def burkes(self):
        self.image = filters.useFilter(self.image, self.var.get(), 'burkes')
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the stucky button
    def stucky(self):
        self.image = filters.useFilter(self.image, self.var.get(), 'stucky')
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the sierra button
    def sierra(self):
        self.image = filters.useFilter(self.image, self.var.get(), 'sierra')
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the atkinson button
    def atkinson(self):
        self.image = filters.useFilter(self.image, self.var.get(), 'atkinson')
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the quant button
    def uniformQuantization(self):
        self.image = uniformQunatization.quantize(self.image, self.slider.get())
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


# Create a root and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
