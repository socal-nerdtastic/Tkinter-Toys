#!/usr/bin/env python3
#
# version 2025-05-15

import tkinter as tk
from tkinter import ttk

def recursive_change_state(widget, new_state):
    if hasattr(widget, 'children'):
        for child in widget.children.values():
            recursive_change_state(child, new_state)
    try:
        widget.config(state=new_state)
    except Exception as e:
        pass

class CheckbuttonLabelFrame(ttk.LabelFrame):
    """A LabelFrame with a Checkbutton in the title
    command is executed when user check the button manually only"""
    def __init__(self, parent=None, text="", command:callable=None, variable:tk.Variable=None, **kwargs):
        self.command = command
        self.variable = variable or tk.BooleanVar(value=True)
        self.title = tk.Checkbutton(parent, text=text, variable=self.variable, command=self.on_click)
        super().__init__(parent, labelwidget=self.title, **kwargs)
        self.get, self.set = self.variable.get, self.variable.set
    def on_click(self):
        if self.command:
            self.command(self.get())

class EnableLabelFrame(CheckbuttonLabelFrame):
    """A LabelFrame with a Checkbutton in the title
    the checkbutton enables or disables the content of the frame"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable.trace_add('write', self.on_configure)
        self.bind('<Configure>', self.on_configure)
    def on_configure(self, *args):
        # triggered by configure event (adding stuff) OR checkbutton
        # triggers BEFORE parent.on_click
        state = tk.NORMAL if self.get() else tk.DISABLED
        recursive_change_state(self, state)

class CollapsingLabelFrame:
    """A LabelFrame with a Checkbutton in the title
    the checkbutton hides or unhides the content of the frame"""
    def __init__(self, parent=None, **kwargs):
        self.outer = CheckbuttonLabelFrame(parent, **kwargs)
        self.outer.variable.trace_add('write', self.on_configure)
        self.inner = tk.Frame(self.outer)
        self.inner.pack(fill=tk.BOTH, expand=True)
        self.inner.bind('<Configure>', self.on_configure)
        self.outer_attr = set(dir(tk.Widget))
        self.blank = tk.Frame(self.outer)
        self.get, self.set = self.outer.get, self.outer.set
    def on_configure(self, *args):
        if self.outer.variable.get():
            self.inner.pack(fill=tk.BOTH)
            self.blank.pack_forget()
        else:
            self.inner.pack_forget()
            self.blank.pack()
    def __getattr__(self, item):
        if item in self.outer_attr:
            return getattr(self.outer, item)
        else:
            return getattr(self.inner, item)

def testlabels(frm):
    for i in range(3):
        lbl = tk.Label(frm, text=f"hello world, this is label number {i}")
        lbl.pack(fill=tk.X)
    ent = ttk.Entry(frm)
    ent.pack(fill=tk.X)
    ent.insert(0, "Example entry")
    ttk.Button(frm, text="Test button").pack(fill=tk.X)

def test():
    from functools import partial

    r = tk.Tk()

    frm = CheckbuttonLabelFrame(r, text="Checkbutton frame", command=print)
    testlabels(frm)
    frm.grid(row=0, column=0, sticky='nw', padx=2, pady=2)

    frm = EnableLabelFrame(r, text="Enable/disable frame", command=print)
    testlabels(frm)
    frm.grid(row=0, column=1, sticky='nw', padx=2, pady=2)

    frm = CollapsingLabelFrame(r, text="Show/hide frame", command=print)
    testlabels(frm)
    frm.grid(row=0, column=2, sticky='nw', padx=2, pady=2)

    frm = CheckbuttonLabelFrame(r, text="Checkbutton frame", command=print)
    testlabels(frm)
    frm.grid(row=1, column=0, sticky='nw', padx=2, pady=2)
    frm.set(False)

    btn = ttk.Button(r, text='check', command=partial(frm.set,True))
    btn.grid(row=2, column=0)
    btn = ttk.Button(r, text='uncheck', command=partial(frm.set,False))
    btn.grid(row=3, column=0)

    frm = EnableLabelFrame(r, text="Enable/disable frame", command=print)
    testlabels(frm)
    frm.grid(row=1, column=1, sticky='nw', padx=2, pady=2)
    frm.set(False)

    btn = ttk.Button(r, text='enable', command=partial(frm.set,True))
    btn.grid(row=2, column=1)
    btn = ttk.Button(r, text='disable', command=partial(frm.set,False))
    btn.grid(row=3, column=1)

    frm = CollapsingLabelFrame(r, text="Show/hide frame", command=print)
    testlabels(frm)
    frm.grid(row=1, column=2, sticky='nw', padx=2, pady=2)
    frm.set(False)

    btn = ttk.Button(r, text='expand', command=partial(frm.set,True))
    btn.grid(row=2, column=2)
    btn = ttk.Button(r, text='collapse', command=partial(frm.set,False))
    btn.grid(row=3, column=2)

    r.mainloop()

if __name__ == "__main__":
    test()
    pass

