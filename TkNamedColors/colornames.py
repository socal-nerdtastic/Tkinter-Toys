#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   from: http://wiki.tcl.tk/16166
#

# stolen from https://github.com/novel-yet-trivial/TkNamedColors

# but I have no reservations about changing the code ... so I added a few features:
# - click a color to copy the name

try:
    import Tkinter as tk
    from tkMessageBox import showinfo
except:
    import tkinter as tk
    from tkinter.messagebox import showinfo

COLORS = [
    "snow", "ghost white", "white smoke", "gainsboro", "floral white",
    "old lace", "linen", "antique white", "papaya whip", "blanched almond",
    "bisque", "peach puff", "navajo white", "moccasin", "cornsilk", "ivory",
    "lemon chiffon", "seashell", "honeydew", "mint cream", "azure",
    "alice blue", "lavender", "lavender blush", "misty rose", "white", "black",
    "dark slate gray", "dim gray", "slate gray", "light slate gray", "gray",
    "light grey", "midnight blue", "navy", "cornflower blue", "dark slate blue",
    "slate blue", "medium slate blue", "light slate blue", "medium blue",
    "royal blue", "blue", "dodger blue", "deep sky blue", "sky blue",
    "light sky blue", "steel blue", "light steel blue", "light blue",
    "powder blue", "pale turquoise", "dark turquoise", "medium turquoise",
    "turquoise", "cyan", "light cyan", "cadet blue", "medium aquamarine",
    "aquamarine", "dark green", "dark olive green", "dark sea green",
    "sea green", "medium sea green", "light sea green", "pale green",
    "spring green", "lawn green", "green", "chartreuse", "medium spring green",
    "green yellow", "lime green", "yellow green", "forest green", "olive drab",
    "dark khaki", "khaki", "pale goldenrod", "light goldenrod yellow",
    "light yellow", "yellow", "gold", "light goldenrod", "goldenrod",
    "dark goldenrod", "rosy brown", "indian red", "saddle brown", "sienna",
    "peru", "burlywood", "beige", "wheat", "sandy brown", "tan", "chocolate",
    "firebrick", "brown", "dark salmon", "salmon", "light salmon", "orange",
    "dark orange", "coral", "light coral", "tomato", "orange red", "red",
    "hot pink", "deep pink", "pink", "light pink", "pale violet red", "maroon",
    "medium violet red", "violet red", "magenta", "violet", "plum", "orchid",
    "medium orchid", "dark orchid", "dark violet", "blue violet", "purple",
    "medium purple", "thistle", "snow2", "snow3", "snow4", "seashell2",
    "seashell3", "seashell4", "AntiqueWhite1", "AntiqueWhite2", "AntiqueWhite3",
    "AntiqueWhite4", "bisque2", "bisque3", "bisque4", "PeachPuff2", "PeachPuff3",
    "PeachPuff4", "NavajoWhite2", "NavajoWhite3", "NavajoWhite4",
    "LemonChiffon2", "LemonChiffon3", "LemonChiffon4", "cornsilk2", "cornsilk3",
    "cornsilk4", "ivory2", "ivory3", "ivory4", "honeydew2", "honeydew3",
    "honeydew4", "LavenderBlush2", "LavenderBlush3", "LavenderBlush4",
    "MistyRose2", "MistyRose3", "MistyRose4", "azure2", "azure3", "azure4",
    "SlateBlue1", "SlateBlue2", "SlateBlue3", "SlateBlue4", "RoyalBlue1",
    "RoyalBlue2", "RoyalBlue3", "RoyalBlue4", "blue2", "blue4", "DodgerBlue2",
    "DodgerBlue3", "DodgerBlue4", "SteelBlue1", "SteelBlue2", "SteelBlue3",
    "SteelBlue4", "DeepSkyBlue2", "DeepSkyBlue3", "DeepSkyBlue4", "SkyBlue1",
    "SkyBlue2", "SkyBlue3", "SkyBlue4", "LightSkyBlue1", "LightSkyBlue2",
    "LightSkyBlue3", "LightSkyBlue4", "SlateGray1", "SlateGray2", "SlateGray3",
    "SlateGray4", "LightSteelBlue1", "LightSteelBlue2", "LightSteelBlue3",
    "LightSteelBlue4", "LightBlue1", "LightBlue2", "LightBlue3", "LightBlue4",
    "LightCyan2", "LightCyan3", "LightCyan4", "PaleTurquoise1", "PaleTurquoise2",
    "PaleTurquoise3", "PaleTurquoise4", "CadetBlue1", "CadetBlue2", "CadetBlue3",
    "CadetBlue4", "turquoise1", "turquoise2", "turquoise3", "turquoise4",
    "cyan2", "cyan3", "cyan4", "DarkSlateGray1", "DarkSlateGray2",
    "DarkSlateGray3", "DarkSlateGray4", "aquamarine2", "aquamarine4",
    "DarkSeaGreen1", "DarkSeaGreen2", "DarkSeaGreen3", "DarkSeaGreen4",
    "SeaGreen1", "SeaGreen2", "SeaGreen3", "PaleGreen1", "PaleGreen2",
    "PaleGreen3", "PaleGreen4", "SpringGreen2", "SpringGreen3", "SpringGreen4",
    "green2", "green3", "green4", "chartreuse2", "chartreuse3", "chartreuse4",
    "OliveDrab1", "OliveDrab2", "OliveDrab4", "DarkOliveGreen1",
    "DarkOliveGreen2", "DarkOliveGreen3", "DarkOliveGreen4", "khaki1", "khaki2",
    "khaki3", "khaki4", "LightGoldenrod1", "LightGoldenrod2", "LightGoldenrod3",
    "LightGoldenrod4", "LightYellow2", "LightYellow3", "LightYellow4",
    "yellow2", "yellow3", "yellow4", "gold2", "gold3", "gold4", "goldenrod1",
    "goldenrod2", "goldenrod3", "goldenrod4", "DarkGoldenrod1",
    "DarkGoldenrod2", "DarkGoldenrod3", "DarkGoldenrod4", "RosyBrown1",
    "RosyBrown2", "RosyBrown3", "RosyBrown4", "IndianRed1", "IndianRed2",
    "IndianRed3", "IndianRed4", "sienna1", "sienna2", "sienna3", "sienna4",
    "burlywood1", "burlywood2", "burlywood3", "burlywood4", "wheat1", "wheat2",
    "wheat3", "wheat4", "tan1", "tan2", "tan4", "chocolate1", "chocolate2",
    "chocolate3", "firebrick1", "firebrick2", "firebrick3", "firebrick4",
    "brown1", "brown2", "brown3", "brown4", "salmon1", "salmon2", "salmon3",
    "salmon4", "LightSalmon2", "LightSalmon3", "LightSalmon4", "orange2",
    "orange3", "orange4", "DarkOrange1", "DarkOrange2", "DarkOrange3",
    "DarkOrange4", "coral1", "coral2", "coral3", "coral4", "tomato2", "tomato3",
    "tomato4", "OrangeRed2", "OrangeRed3", "OrangeRed4", "red2", "red3", "red4",
    "DeepPink2", "DeepPink3", "DeepPink4", "HotPink1", "HotPink2", "HotPink3",
    "HotPink4", "pink1", "pink2", "pink3", "pink4", "LightPink1", "LightPink2",
    "LightPink3", "LightPink4", "PaleVioletRed1", "PaleVioletRed2",
    "PaleVioletRed3", "PaleVioletRed4", "maroon1", "maroon2", "maroon3",
    "maroon4", "VioletRed1", "VioletRed2", "VioletRed3", "VioletRed4",
    "magenta2", "magenta3", "magenta4", "orchid1", "orchid2", "orchid3",
    "orchid4", "plum1", "plum2", "plum3", "plum4", "MediumOrchid1",
    "MediumOrchid2", "MediumOrchid3", "MediumOrchid4", "DarkOrchid1",
    "DarkOrchid2", "DarkOrchid3", "DarkOrchid4", "purple1", "purple2",
    "purple3", "purple4", "MediumPurple1", "MediumPurple2", "MediumPurple3",
    "MediumPurple4", "thistle1", "thistle2", "thistle3", "thistle4", "gray1",
    "gray2", "gray3", "gray4", "gray5", "gray6", "gray7", "gray8", "gray9",
    "gray10", "gray11", "gray12", "gray13", "gray14", "gray15", "gray16",
    "gray17", "gray18", "gray19", "gray20", "gray21", "gray22", "gray23",
    "gray24", "gray25", "gray26", "gray27", "gray28", "gray29", "gray30",
    "gray31", "gray32", "gray33", "gray34", "gray35", "gray36", "gray37",
    "gray38", "gray39", "gray40", "gray42", "gray43", "gray44", "gray45",
    "gray46", "gray47", "gray48", "gray49", "gray50", "gray51", "gray52",
    "gray53", "gray54", "gray55", "gray56", "gray57", "gray58", "gray59",
    "gray60", "gray61", "gray62", "gray63", "gray64", "gray65", "gray66",
    "gray67", "gray68", "gray69", "gray70", "gray71", "gray72", "gray73",
    "gray74", "gray75", "gray76", "gray77", "gray78", "gray79", "gray80",
    "gray81", "gray82", "gray83", "gray84", "gray85", "gray86", "gray87",
    "gray88", "gray89", "gray90", "gray91", "gray92", "gray93", "gray94",
    "gray95", "gray97", "gray98", "gray99"
]

WINDOWSCOLORS = [
  'SystemButtonFace', 'SystemButtonText', 'SystemDisabledText',
  'SystemHighlight', 'SystemHightlightText', 'SystemMenu', 'SystemMenuText',
  'SystemScrollbar', 'SystemWindow', 'SystemWindowFrame', 'SystemWindowText'
]

class S:
    w = 130 # width of a single element
    h = 20 # height of a single element
    wrap = -1

def DrawColors(event=None):
    fill = ['black', 'white']
    cwidth = c.winfo_width()
    wrap = (cwidth - 20) // S.w
    if wrap <= 0: wrap = 1
    if wrap == S.wrap: return # no need to redraw
    S.wrap = wrap

    c.delete('all')

    for cnt, color in enumerate(COLORS + WINDOWSCOLORS):
        color = ' '.join(color.split())
        try: rgb = root.winfo_rgb(color)
        except tk.TclError: continue

        # Convert to HSV and get the V value to determine fill color
        # see [Selecting visually different RGB colors]
        value = max(rgb)
        value = value / 65535.0

        tag = "i%d"%cnt
        row, col = divmod(cnt, wrap)
        x1 = 10 + col * S.w
        y1 = 10 + row * S.h
        x2 = x1 + S.w
        y2 = y1 + S.h
        xc = (x1 + x2) / 2.0
        yc = (y1 + y2) / 2.0
        c.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, tag=tag)
        c.create_text(xc, yc, text=color, tag=['txt', tag], fill=fill[value<0.6])

        # rgb2 = "#%04X%04X%04X"%(rgb) # 16 bit RGB
        rgb2 = root.eval('::tk::Darken "%s" 100'%color) # 8 bit RGB

        rgb = ' / '.join(map(str, rgb))
        c.tag_bind(tag, '<Enter>', lambda e, m="%s => %s => %s"%(color, rgb, rgb2): S.msg.set(m))
        c.tag_bind(tag, '<Double-Button-1>', lambda e, c=color: Clipit(c))
    c.config(scrollregion=c.bbox('all'))
    c.tag_raise('txt')

def Clipit(color):
    root.clipboard_clear()
    root.clipboard_append(color)

root = tk.Tk()
root.title('Tk Named Colors')
c = tk.Canvas(root, width=670, height=600)
sby = tk.Scrollbar(root, orient=tk.VERTICAL, command=c.yview)
c.config(yscrollcommand=sby.set)
S.msg = tk.StringVar()
msg = tk.Label(root, textvariable=S.msg, relief=tk.SUNKEN, bg='white')
img = tk.PhotoImage(width=1, height=1)
about = tk.Button(image=img, highlightthickness=0,
    command = lambda: showinfo(message="Tk Named Colors\nby Keith Vetter, March 2003"))
about.place(in_=msg, relx=1, rely=1, anchor='se')

c.grid(row=0, column=0, sticky='news')
sby.grid(row=0, column=1, sticky='ns')
msg.grid(sticky='ew')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
c.bind('<Configure>', DrawColors)
root.mainloop()
