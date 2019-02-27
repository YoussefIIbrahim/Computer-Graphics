import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from Filters import filters
class App:
    def __init__(self, window, window_title, image_path="eye.jpg"):
        self.window = window
        self.window.title(window_title)

        # Load an image using OpenCV
        self.cv_img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_img.shape

        # Create a canvas that can fit the above image
        self.canvas = tkinter.Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.bottomFrame = tkinter.Frame()
        self.bottomFrame.pack()

        # Button for inversion
        self.btn_inversion = tkinter.Button(self.bottomFrame, text="Inversion", width=50, command=self.invert_image)
        self.btn_inversion.grid(row=0)

        # Button for brightness
        self.btn_bright = tkinter.Button(self.bottomFrame, text="Brightness Correction", width=50, command=self.brightness)
        self.btn_bright.grid(row=0, column=1)

        # Button for contrast
        self.btn_contrast = tkinter.Button(self.bottomFrame, text="Blur", width=50, command=self.contrast)
        self.btn_contrast.grid(row=0)

        # Button for gamma
        self.btn_gamma = tkinter.Button(self.bottomFrame, text="Blur", width=50, command=self.Gamma)
        self.btn_gamma.grid(row=0, column=1)

        # Button for blur
        self.btn_blur = tkinter.Button(self.bottomFrame, text="Blur", width=50, command=self.blur_image)
        self.btn_blur.grid(row=0)

        # Gaussian
        self.btn_gaussian = tkinter.Button(self.bottomFrame, text="Blur", width=50, command=self.gaussian_blur)
        self.btn_gaussian.grid(row=0, column=1)

        # Sharpen
        self.btn_sharpen = tkinter.Button(self.bottomFrame, text="Blur", width=50, command=self.sharpen)
        self.btn_sharpen.grid(row=0, column=1)

        # Edge Detection
        self.btn_edge_detection = tkinter.Button(self.bottomFrame, text="Blur", width=50, command=self.edge_detection)
        self.btn_edge_detection.grid(row=0, column=1)

        # Emboss
        self.btn_emboss = tkinter.Button(self.bottomFrame, text="Blur", width=50, command=self.emboss)
        self.btn_emboss.grid(row=0, column=1)

        self.window.mainloop()

    # Callback for the "Blur" button
    def blur_image(self):
        self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")