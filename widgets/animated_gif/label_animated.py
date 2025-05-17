#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import count, cycle
from pathlib import Path

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, (str, Path)):
            im = Image.open(im)
        self.frames = []
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            self.frame_iter = cycle(self.frames)
        self.delay = im.info.get('duration', 100)

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
            self.frames = None
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frame_iter))
            self.after(self.delay, self.next_frame)

# DEMO:
def demo():
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

if __name__ == "__main__":
    demo()
