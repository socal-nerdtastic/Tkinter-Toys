#!/usr/bin/env python3
#
#  Copyright 2025 j.brauer <j.brauer@bruker.com>
#
#  This program is internal property of Bruker Nano, and may not be distributed.
#  2025-02-14-0945.py
#

import tkinter as tk

def keyprint(event):
    for name in dir(event):
        if name.startswith("__"):
            continue
        val = getattr(event, name)
        print(f"{name} = {val!r}")
    print()

root = tk.Tk()
root.bind("<Key>", keyprint) # bind all keypresses
root.mainloop()
