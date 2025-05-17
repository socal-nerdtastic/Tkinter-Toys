#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import count

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, (str, Path)):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

# DEMO:
def demo():
    pass

from pathlib import Path
from itertools import cycle

images = cycle(Path('imgs').iterdir())

root = tk.Tk()
lbl = ImageLabel(root)
lbl.pack(side=tk.LEFT)
lbl.load(next(images))
btns = tk.Frame(root)
ttk.Button(btns, text="next", command=lambda:lbl.load(next(images))).pack()
ttk.Button(btns, text="unload", command=lbl.unload).pack()
btns.pack(side=tk.LEFT, padx=20)
root.mainloop()

