#!/usr/bin/env python3

from pathlib import Path
import time
import sys

import tkinter as tk

DEBUG = True

def dprint(*args, **kwargs):
    if DEBUG:
        print(time.strftime("%Y-%m-%d, %H:%M:%S"), *args, **kwargs)

class GeoKeeper:
    """this code will remember the geometry of your program the next time it loads
    if the last geometry is off the screen, it will not apply it"""
    def __init__(self, root, prog_name):
        self.tk_root = root or tk._default_root
        self.settingsfile = Path.home() / f".{prog_name}_geosettings.txt"
        self.tk_root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.on_load()

    def load_settings(self):
        try:
            with open(self.settingsfile) as f:
                return f.readline().strip()
        except FileNotFoundError:
            dprint(f"Failed to load ({self.settingsfile}) - File not found")

    def save_settings(self, geosettings):
        try:
            with open(self.settingsfile, 'w') as f:
                print(geosettings, file=f)
        except FileNotFoundError:
            dprint(f"Cannot save file ({self.settingsfile}) - Settings folder not found")

    def on_exit(self):
        geosettings = self.tk_root.geometry()
        self.save_settings(geosettings)
        self.tk_root.destroy()
        self.tk_root.quit()

    def win11hack(self, geo):
        "windows 11 won't config the graphic without a tiny change to the size"
        if sys.platform == "linux":
            return # not needed
        width, rest = geo.split("x")
        if (w := int(width)) & 1:
            w += 1
        else:
            w -= 1
        self.tk_root.after(200, self.tk_root.geometry, f"{w}x{rest}")
        dprint("geo windows hack activated")

    def on_load(self):
        """set the given geometry if it's not out of range of the current display"""
        geo = self.load_settings()
        if not geo:
            return # no settings file
        winsize, left_pos, top_pos = geo.split("+")
        width, height = winsize.split("x")
        left_pos, top_pos, width, height = map(int, (left_pos, top_pos, width, height))
        right_pos = left_pos + width
        bottom_pos = top_pos + height
        dprint("geometry:", (left_pos, top_pos, width, height, right_pos, bottom_pos))

        if (
            left_pos < self.tk_root.winfo_vrootx() or
            right_pos > (self.tk_root.winfo_vrootx() + self.tk_root.winfo_vrootwidth()) or
            top_pos < self.tk_root.winfo_rooty() or
            bottom_pos > (self.tk_root.winfo_rooty() + self.tk_root.winfo_vrootheight())
            ):
                return dprint("out of current bounds")
        self.tk_root.geometry(geo)
        self.win11hack(geo)

def test():
    root = tk.Tk()
    GeoKeeper(root, "geotesterV1")
    tk.Label(text="resize this window\nthen close it and rerun\n\nwindow size and position\nwill be remembered").pack()
    root.mainloop()

if __name__ == "__main__":
    test()
