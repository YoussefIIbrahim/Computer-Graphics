import tkinter


class Circle(tkinter.Toplevel):
    def __init__(self, parent):
        tkinter.Toplevel.__init__(self)
        self.grab_set()
        self.parent = parent
        self.title('Circle')

        tkinter.Label(self, text='Center coordinate').grid(row=0, column=0, columnspan=2, padx=40)

        self.x = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.x.insert(0, 0)
        self.x.grid(row=1, column=0)

        self.y = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.y.insert(0, 0)
        self.y.grid(row=1, column=1)

        tkinter.Label(self, text='Radius').grid(row=2, column=0, columnspan=2)

        self.rad = tkinter.Entry(self, width=6, borderwidth=4, relief="ridge")
        self.rad.insert(0, 0)
        self.rad.grid(row=3, column=0)

        tkinter.Button(self, text='Apply', command=self.apply).grid(row=4, column=0, columnspan=2, pady=10)

    def apply(self):
        self.parent.draw_circle(int(self.x.get()), int(self.y.get()), int(self.rad.get()))
