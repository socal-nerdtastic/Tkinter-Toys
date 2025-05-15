#!/usr/bin/env python3
#
# version 2025-05-15

from pathlib import Path
import time
import sys

import tkinter as tk

DEBUG = False

def dprint(*args, **kwargs):
    if DEBUG:
        print(time.strftime("%Y-%m-%d, %H:%M:%S"), *args, **kwargs)

def win11hack(root:tk.Tk, geo:str):
    "windows 11 won't config the graphic without a tiny change to the size"
    if sys.platform == "linux":
        return # not needed
    width, rest = geo.split("x")
    w = int(width)
    w += 1 if w&1 else -1
    root.after(200, root.geometry, f"{w}x{rest}")
    dprint("geo windows hack activated")

def geometry_try(root:tk.Tk, geo:str):
    """attempt to apply the given geometry to the root window
    if it's not out of range of the current display"""
    if not geo:
         return # nothing to do :/
    winsize, left_pos, top_pos = geo.split("+")
    width, height = winsize.split("x")
    left_pos, top_pos, width, height = map(int, (left_pos, top_pos, width, height))
    right_pos = left_pos + width
    bottom_pos = top_pos + height
    dprint("geometry:", (left_pos, top_pos, width, height, right_pos, bottom_pos))

    if (
        left_pos < root.winfo_vrootx() or
        right_pos > (root.winfo_vrootx() + root.winfo_vrootwidth()) or
        top_pos < root.winfo_rooty() or
        bottom_pos > (root.winfo_rooty() + root.winfo_vrootheight())
        ):
            return dprint("out of current bounds")
    root.geometry(geo)
    win11hack(root, geo)

class GeoKeeper:
    """this code will remember the geometry of your program the next time it loads.
    if the last geometry is off the screen, it will not apply it"""
    def __init__(self, root=None, prog_name="geokeeper"):
        self.tk_root = root or tk._default_root
        self.tk_root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.settingsfile = Path.home() / f".{prog_name}_geosettings.txt"
        if self.settingsfile.exists():
            last_geometry = self.settingsfile.read_text().strip()
            geometry_try(self.tk_root, last_geometry)
        else:
            dprint(f"Failed to load ({self.settingsfile}) - File not found")

    def on_exit(self):
        geosettings = self.tk_root.geometry()
        try:
            self.settingsfile.write_text(geosettings)
        except Exception as e:
            dprint(f"Cannot save file ({self.settingsfile}) - {e}")
        self.tk_root.destroy()
        self.tk_root.quit()

def minimaltest():
    '''what you should probably use if you already have a settings file'''
    geotester_file = Path.home() / ".geotester.txt"
    def on_close():
         geotester_file.write_text(r.geometry())
         r.destroy()
    r = tk.Tk()
    r.protocol("WM_DELETE_WINDOW", on_close)
    if geotester_file.exists():
        geometry_try(r, geotester_file.read_text())
    r.mainloop()

def test():
    r = tk.Tk()
    GeoKeeper(root=r, prog_name="geotester") # this line is all you need to add to your code.
    # ~ GeoKeeper() #  root and prog_name are optional; this also works
    tk.Label(text="resize this window\nthen close it and rerun\n\nwindow size and position\nwill be remembered").pack()
    r.mainloop()

if __name__ == "__main__":
    test()
