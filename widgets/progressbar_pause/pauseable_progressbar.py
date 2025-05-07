#!/usr/bin/env python3

# a demo of a progressbar that can be paused and reset.

import tkinter as tk
from tkinter import ttk

def tick(*args):
    # var will loop over range(100) {so 0 - 99, inclusive} by default
    if var.get() >= 99: # could also use `prog_bar['value']`. The Variable is required for the command to be triggered, so may as well use it here too.
        prog_bar.stop()
        start_btn['text'] = "Restart"
    elif var.get() >= 65:
        prog_bar['style'] = 'red.Horizontal.TProgressbar'
    elif var.get() >= 35:
        prog_bar['style'] = 'yellow.Horizontal.TProgressbar'
    else:
        prog_bar['style'] = 'Horizontal.TProgressbar'

def start_timer():
    if start_btn['text'] in ("Start", "Unpause", "Restart"):
        prog_bar.start(interval=100)
        start_btn['text'] = "Pause"
    elif start_btn['text'] == "Pause":
        prog_bar.stop()
        start_btn['text'] = "Unpause"

def reset_timer():
    prog_bar.stop()
    start_btn['text'] = "Start"
    var.set(0)

# DEMO:
root = tk.Tk()

style = ttk.Style()
style.configure("red.Horizontal.TProgressbar", background="red")
style.configure("yellow.Horizontal.TProgressbar", background="yellow")
var = tk.IntVar()
var.trace('w', tick)
prog_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, variable=var)
prog_bar.pack()
start_btn = ttk.Button(text="Start", command=start_timer)
start_btn.pack()
btn = ttk.Button(text="Reset", command=reset_timer)
btn.pack()

root.mainloop()
