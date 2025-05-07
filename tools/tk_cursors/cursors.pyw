#!/usr/bin/env python3

# From: https://www.tcl.tk/man/tcl8.4/TkCmd/cursors.html
cursors = dict(
    tcl_cursors = """\
    X_cursor
    arrow
    based_arrow_down
    based_arrow_up
    boat
    bogosity
    bottom_left_corner
    bottom_right_corner
    bottom_side
    bottom_tee
    box_spiral
    center_ptr
    circle
    clock
    coffee_mug
    cross
    cross_reverse
    crosshair
    diamond_cross
    dot
    dotbox
    double_arrow
    draft_large
    draft_small
    draped_box
    exchange
    fleur
    gobbler
    gumby
    hand1
    hand2
    heart
    icon
    iron_cross
    left_ptr
    left_side
    left_tee
    leftbutton
    ll_angle
    lr_angle
    man
    middlebutton
    mouse
    pencil
    pirate
    plus
    question_arrow
    right_ptr
    right_side
    right_tee
    rightbutton
    rtl_logo
    sailboat
    sb_down_arrow
    sb_h_double_arrow
    sb_left_arrow
    sb_right_arrow
    sb_up_arrow
    sb_v_double_arrow
    shuttle
    sizing
    spider
    spraycan
    star
    target
    tcross
    top_left_arrow
    top_left_corner
    top_right_corner
    top_side
    top_tee
    trek
    ul_angle
    umbrella
    ur_angle
    watch
    xterm""",
    windows_native = """\
    arrow
    center_ptr
    crosshair
    fleur
    ibeam
    icon
    sb_h_double_arrow
    sb_v_double_arrow
    watch
    xterm""",
    windows_additional = """\
    no
    starting
    size
    size_ne_sw
    size_ns
    size_nw_se
    size_we
    uparrow
    wait""",
    # The no cursor can be specified to eliminate the cursor.
    mac_native = """\
    arrow
    cross
    crosshair
    ibeam
    plus
    watch
    xterm""",
    mac_additional = """\
    copyarrow
    aliasarrow
    contextualmenuarrow
    text
    cross-hair
    closedhand
    openhand
    pointinghand
    resizeleft
    resizeright
    resizeleftright
    resizeup
    resizedown
    resizeupdown
    none
    notallowed
    poof
    countinguphand
    countingdownhand
    countingupanddownhand
    spinning"""
)

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

COLS = 8
root = tk.Tk()
for section in cursors:
    tk_section = tk.LabelFrame(text=section)
    tk_section.pack(anchor=tk.W)
    for i, cur in enumerate(cursors[section].splitlines()):
        cur = cur.strip()
        if cur:
            try:
                lbl = tk.Label(tk_section, text=cur, cursor=cur)
            except Exception as e:
                lbl = tk.Label(tk_section, text=cur, fg='red')
            lbl.grid(row=i//COLS, column=i%COLS)

root.mainloop()
