import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from Filters import filters


class App:
    def __init__(self, window, window_title, image_path="eye.jpg"):
        self.window = window
        self.window.title(window_title)

        self.topFrame = tkinter.Frame()
        self.topFrame.pack()

        # Load an image using OpenCV
        self.cv_img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_img.shape

        # Create a canvas that can fit the above image
        self.canvasOne = tkinter.Canvas(self.topFrame, width = self.width, height = self.height)
        self.canvasOne.grid(row=0, column=0)

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photoOne = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))

        # Add a PhotoImage to the Canvas
        self.canvasOne.create_image(0, 0, image=self.photoOne, anchor=tkinter.NW)

        # Create a canvas that can fit the edited image
        self.canvas = tkinter.Canvas(self.topFrame, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=1)

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))
        #
        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.bottomFrame = tkinter.Frame()
        self.bottomFrame.pack()

        # Button for inversion
        self.btn_inversion = tkinter.Button(self.bottomFrame, text="Inversion", width=50, command=self.invert_image)
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

        self.window.mainloop()

    # Callback for the "Blur" button
    def invert_image(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def brightness(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def contrast(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def blur_image(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def gamma(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def gaussian_blur(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def sharpen(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def edge_detection(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Callback for the "Blur" button
    def emboss(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV", )