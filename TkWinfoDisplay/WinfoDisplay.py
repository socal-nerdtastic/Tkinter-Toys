#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#
#   from: https://www.reddit.com/r/learnpython/comments/kbt1c8/help_tkinter_eventx_and_eventy_coords_changes/
#   Reddit user: Re-Modu
#   2020-12-12-1118-Re-Modu.py

import tkinter as tk
winfo_attributes = ['winfo_cells',
'winfo_children', 'winfo_class', 'winfo_colormapfull',
 'winfo_depth', 'winfo_exists',
 'winfo_geometry', 'winfo_height', 'winfo_id', 'winfo_interps',
 'winfo_ismapped', 'winfo_manager', 'winfo_name', 'winfo_parent',
 'winfo_pointerx', 'winfo_pointerxy',
 'winfo_pointery', 'winfo_reqheight', 'winfo_reqwidth',
  'winfo_rootx', 'winfo_rooty', 'winfo_screen', 'winfo_screencells',
  'winfo_screendepth', 'winfo_screenheight', 'winfo_screenmmheight',
  'winfo_screenmmwidth', 'winfo_screenvisual', 'winfo_screenwidth',
   'winfo_server', 'winfo_toplevel', 'winfo_viewable', 'winfo_visual',
   'winfo_visualid', 'winfo_vrootheight',
   'winfo_vrootwidth', 'winfo_vrootx', 'winfo_vrooty', 'winfo_width',
   'winfo_x', 'winfo_y']
winfo_attributes_not_displayed = ['winfo_children']
for atr in winfo_attributes_not_displayed:
    winfo_attributes.remove(atr)
event_attributes = ['char', 'delta', 'height', 'keycode', 'keysym', 'keysym_num', 'num', 'send_event', 'serial', 'state', 'time', 'type', 'widget', 'width', 'x', 'x_root', 'y', 'y_root']

def update_bg(event=None):
    result = ""
    for atr in winfo_attributes:
        result += f'{atr}: {getattr(root,atr)()}\n'
    wlbl.config(text=result)

    result = ""
    for atr in event_attributes:
        result += f'{atr}: {getattr(event,atr)}\n'
    elbl.config(text=result)

root = tk.Tk()
# ~ root.geometry('300x600')
root.bind("<Motion>", update_bg)
wlbl = tk.Label(root, font=('',10))
wlbl.pack(side=tk.LEFT)
elbl = tk.Label(root, font=('',10))
elbl.pack()
btn = tk.Button(text="Don't click me, I'm not connected!")
btn.pack(side=tk.BOTTOM)

root.mainloop()
