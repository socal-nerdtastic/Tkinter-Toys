#!/usr/bin/env python3
#
# TODO: Add scroll bars or zoom to image view for large images.
# TODO: add dialog when load fails
# TODO: add support for other image formats

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from functools import partial

SIZE = "800x500" # window start size and position

class GUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.refs = []
        self.start = None
        self.current = ''
        self.image = None
        self.trash_img = tk.PhotoImage(data=delete_graphic)

        topframe = tk.Frame(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        topframe.grid(columnspan=2, sticky='ew')
        btn = ttk.Button(topframe, text='Clear & Load', command=self.load)
        btn.pack(side=tk.LEFT)
        self.filename_lbl = tk.Label(topframe)
        self.filename_lbl.pack(side=tk.LEFT)
        self.c = tk.Canvas(self, bg='white')
        self.c.grid(sticky='nsew', rowspan=2)
        self.c.bind("<Button>", self.on_click)
        self.c.bind("<ButtonRelease>", self.on_release)
        self.c.bind("<Motion>", self.on_motion)
        self.output = ScrolledText(self, width=22)
        self.output.grid(row=1, column=1, sticky='ns')
        self.output.insert(0.0,'X0,Y0,X1,Y1,length\n')
        self.output.tag_config("delete", foreground="red", underline=1)
        # ~ btn = ttk.Button(self, text='Clear', command=self.clear)
        # ~ btn.grid(row=2, column=1)
        self.clear()

    def on_click(self, event):
        self.start = event.x, event.y
        self.current = self.c.create_line(*self.start, *self.start, fill='red', width=2)
        self.refs.append(self.current)

    def on_motion(self, event):
        if self.current:
            self.c.coords(self.current, *self.start, event.x, event.y)

    def on_release(self, event):
        self.on_motion(event)
        length = int(((self.start[0]-event.x)**2  + (self.start[1]-event.y)**2)**0.5)
        data = map(str, self.start+(event.x, event.y,length))
        data = ','.join(data)
        btn = tk.Button(self, image=self.trash_img,
            command=partial(self.on_delete, self.current, data))
        self.output.window_create(tk.END, window=btn)
        self.output.insert(tk.END,data+'\n')
        self.current = None

    def on_delete(self, graphic, line):
        self.c.delete(graphic)
        for i, ref in enumerate(self.output.get(0.0,tk.END).splitlines(),1):
            if line == ref:
                self.output.delete(f'{i}.0',f'{i}.end+1c')
                break

    def clear(self):
        self.output.delete(0.0, tk.END)
        self.output.insert(0.0,'X0,Y0,X1,Y1,length\n')
        self.filename_lbl.config(text='')
        while self.refs:
            self.c.delete(self.refs.pop())

    def load(self):
        fn = askopenfilename(filetypes = (("image files",("*.png", "*.jpg")),("all files","*.*")))
        if not fn: return # user cancelled
        self.clear()
        self.filename_lbl.config(text=fn)
        self.image = tk.PhotoImage(file=fn)
        img_ref= self.c.create_image(0,0,image=self.image,anchor="nw")
        self.refs.append(img_ref)

delete_graphic = '''\
R0lGODlhDgANAMZBAP4AAP8AAP8BAf8DA/8EBP8GBv4ICP8ICP8QEP8REf8UFP8dHf4hIf8hIf8j
I/4kJP4nJ/8rK/4uLv43N/46Ov4/P/5MTP5SUv1VVf1gYP5qav1ra/5ycv1+fv6Bgf6Li/6Pj/6V
lf6bm/6hof6iov6vr/6wsP7AwP7Bwf7ExP7Jyf7Ozv7Y2P7Z2f7b2/7e3v7i4v7l5f7m5v7n5/7x
8f7y8v/y8v7z8//z8//29v739/74+P75+f77+/78/P79/f7+/v//////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////yH5
BAEKAH8ALAAAAAAOAA0AAAeFgEE+NTg6QEFBQDk4Nz+IKwABFDGILAwBBjCIQSEBAR1BPRkBAyWb
QTUXpCcjnho7p0EqDQEPCgESLrGIHweeCCS7iC8OnhE6wkEbAQIBBR7CJgkBFRABCymxMhMBCS0o
BAEWNKccniKIHp4gmyWeGORBMxUBACqIPTY4PJtAOzg1fAQJBAA7
'''

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(SIZE)
    window = GUI(root)
    window.pack(expand=True, fill=tk.BOTH)
    root.mainloop()
