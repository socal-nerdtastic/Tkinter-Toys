#!/usr/bin/env python3
#
#  Copyright 2025 j.brauer <j.brauer@bruker.com>
#
#  This program is internal property of Bruker Nano, and may not be distributed.
#  2025-02-16-2159.py
#

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
from functools import cache
import platform

@cache
def make_radius_imgs(bg, color, size):
    left_top = Image.new("RGB", (size, size), color=bg)
    draw = ImageDraw.Draw(left_top)
    draw.ellipse((0,0,size*2,size*2), fill=color)
    right_top = left_top.transpose(Image.FLIP_LEFT_RIGHT)
    left_bottom = left_top.transpose(Image.FLIP_TOP_BOTTOM)
    right_bottom = right_top.transpose(Image.FLIP_TOP_BOTTOM)

    imgs = left_top,right_top,left_bottom,right_bottom
    return [ImageTk.PhotoImage(img) for img in imgs]

@cache
def blank_img(bg='white'):
    img = Image.new("RGB", (0,0), color=bg)
    return ImageTk.PhotoImage(img)

ALPHA_COLOR = 'green'
CORNER_RADIUS = 20
class RoundedTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = tk.Frame(self)
        self.content.grid(row=1, column=1)
        self.make_border()
        self.overrideredirect(True)
        if platform.system() == "Windows":
            self.wm_attributes("-transparentcolor", ALPHA_COLOR)
        else:
            print("Linux and Mac do not support transparent windows")

    def color_name_to_rgb(self, color):
        if len(color) != 7:
            # convert named color to 16-bit color, and then to 8-bit color
            color = tuple(c>>8 for c in self.winfo_rgb(color))
        return color

    def l_img(self, color, img=None):
        return tk.Label(self, image=img or blank_img(),
            borderwidth=0, bg=color)

    def make_border(self):
        fg_color = self['bg']

        left_top,right_top,left_bottom,right_bottom = make_radius_imgs(
            self.color_name_to_rgb(ALPHA_COLOR),
            self.color_name_to_rgb(fg_color),
            CORNER_RADIUS)

        self.l_img(fg_color, left_top).grid(row=0, column=0, sticky='e') # top left
        self.l_img(fg_color).grid(row=0, column=1, sticky='nsew') # top
        self.l_img(fg_color, right_top).grid(row=0, column=2, sticky='w') # top right

        self.l_img(fg_color).grid(row=1, column=0, sticky='nsew') # left
        self.l_img(fg_color).grid(row=1, column=2, sticky='nsew') # right

        self.l_img(fg_color, left_bottom).grid(row=2, column=0, sticky='e')
        self.l_img(fg_color).grid(row=2, column=1, sticky='nsew') # bottom
        self.l_img(fg_color, right_bottom).grid(row=2, column=2, sticky='w')

root = RoundedTk().content
tk.Label(root, text="example app").pack()
tk.Listbox(root).pack()
ttk.Button(root, text="Quit", command=root.quit).pack()
root.mainloop()
