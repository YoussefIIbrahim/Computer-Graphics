import tkinter


class copyingPixels(tkinter.Toplevel):
    def __init__(self, parent):
        tkinter.Toplevel.__init__(self)
        self.grab_set()
        self.parent = parent
        self.title('Brush')

        tkinter.Label(self, text='First coordinate').grid(row=0, column=0, columnspan=2, padx=40)

        self.x1 = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.x1.insert(0, 0)
        self.x1.grid(row=1, column=0)

        self.y1 = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.y1.insert(0, 0)
        self.y1.grid(row=1, column=1)

        tkinter.Label(self, text='Second coordinate').grid(row=2, column=0, columnspan=2)

        self.x2 = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.x2.insert(0, 0)
        self.x2.grid(row=3, column=0)

        self.y2 = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.y2.insert(0, 0)
        self.y2.grid(row=3, column=1)

        tkinter.Label(self, text='Thickness').grid(row=4, column=0, columnspan=2)

        self.thick = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.thick.insert(0, 1)
        self.thick.grid(row=5, column=0)

        tkinter.Button(self, text='Apply', command=self.apply).grid(row=6, column=0, columnspan=2, pady=10)

    def apply(self):
        self.parent.drawThickLine(int(self.x1.get()), int(self.y1.get()), int(self.x2.get()), int(self.y2.get()),
                                  int(self.thick.get()))
