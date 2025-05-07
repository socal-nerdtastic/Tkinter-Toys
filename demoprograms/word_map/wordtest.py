#!/usr/bin/env python3
#

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from itertools import combinations

START_POS = 50, 50 # the canvas coordinates to place a new word object
START_ZOOMFACTOR = 12
class Word:
    def __init__(self, canvas:tk.Canvas, word:str, size:int=START_ZOOMFACTOR):
        self.can = canvas
        self.word = word
        self.cid = self.can.create_text(*START_POS, font=("", size), text=word)
        self.can.tag_bind(self.cid, "<B1-Motion>", self.move)
    def move(self, event):
        self.can.coords(self.cid, event.x, event.y)
    def coords(self):
        return self.can.coords(self.cid)
    def zoom(self, size):
        self.can.itemconfig(self.cid, font=("", size))

class WordCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.words = []
        self.zoomfactor = START_ZOOMFACTOR
        self.bind("<4>", self._on_mousewheel)
        self.bind("<5>", self._on_mousewheel)
        self.bind("<MouseWheel>", self._on_mousewheel)

        # ~ word = Word(self, 'datainput')
        # ~ self.words.append(word)

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.zoom(-1)
        elif event.num == 5 or event.delta < 0:
            self.zoom(1)

    def zoom(self, inc):
        self.zoomfactor += inc
        for word in self.words:
            word.zoom(self.zoomfactor)

    def add_word(self):
        word = ent.get()
        if not word.strip():
            showerror('error', 'You should type a word in the input box first')
            return
        word = Word(self, ent.get(), self.zoomfactor)
        self.words.append(word)

    def compute(self):
        if len(self.words) < 2:
            output = "you need 2 or more words to calculate distances"
        else:
            output = ''
            for a, b in combinations(self.words, 2):
                # sqrt((x1-x2)^2 + (y1-y2)^2) Pythagoras ftw
                x_a, y_a = a.coords()
                x_b, y_b = b.coords()
                dist = ((x_a-x_b)**2 + (y_a-y_b)**2)**.5
                output += f"{a.word!r} to {b.word!r} = {dist:.2f}\n"
        showinfo("Here's your data", output)

# DEMO:

c = WordCanvas()
c.pack()

bframe = tk.Frame()
ent = ttk.Entry(bframe)
ent.pack(side=tk.LEFT)
btn = ttk.Button(bframe, text="add", command=c.add_word)
btn.pack(side=tk.LEFT)
btn = ttk.Button(bframe, text="Compute", command=c.compute)
btn.pack()
bframe.pack()

c.mainloop()
