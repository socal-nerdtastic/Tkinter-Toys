#!/usr/bin/env python3
#
#  version 2025-05-15

import tkinter as tk
from tkinter import ttk

class SortableListbox(tk.LabelFrame):
    def __init__(self, parent=None, items:list=[], **kwargs):
        super().__init__(parent, **kwargs)

        self.items = items
        self._itemsvar = tk.StringVar(value=self.items)
        self._lb = tk.Listbox(self, listvariable=self._itemsvar)
        self._lb.pack(expand=True, fill=tk.BOTH)

        btmfrm = tk.Frame(self)
        btmfrm.pack(fill=tk.X)
        btn = ttk.Button(btmfrm, text="^", command=self.on_upclick)
        btn.pack(expand=True, fill=tk.X, side=tk.LEFT)
        btn = ttk.Button(btmfrm, text="v", command=self.on_downclick)
        btn.pack(expand=True, fill=tk.X, side=tk.LEFT)

    def on_upclick(self):
        if not (sel := self._lb.curselection()):
            return print('nothing selected')
        idx = sel[0]
        if idx == 0:
            return print("can't move up from 0")
        item = self.items.pop(idx)
        self.items.insert(idx-1, item)
        self._itemsvar.set(self.items)
        self._lb.selection_clear(idx)
        self._lb.selection_set(idx-1)

    def on_downclick(self):
        if not (sel := self._lb.curselection()):
            return print('nothing selected')
        idx = sel[0]
        if idx == len(self.items)-1:
            return print("can't move down from last")
        item = self.items.pop(idx)
        self.items.insert(idx+1, item)
        self._itemsvar.set(self.items)
        self._lb.selection_clear(idx)
        self._lb.selection_set(idx+1)

    def append(self, item):
        self.items.append(item)
        self._itemsvar.set(self.items)

    def replace(self, items):
        self.items[:] = items
        self._itemsvar.set(self.items)

    def extend(self, items):
        self.items.extend(items)
        self._itemsvar.set(self.items)

    def pop(self, idx):
        item = self.items.pop(idx)
        self._itemsvar.set(self.items)
        return item

    def popcurrent(self):
        if not (sel := self._lb.curselection()):
            return print('nothing selected')
        idx = sel[0]
        return self.pop(idx)

class OptionsSelect(tk.LabelFrame):
    def __init__(self, parent=None, leftstart=[], rightstart=[], **kwargs):
        super().__init__(parent, **kwargs)

        self.leftbox = SortableListbox(self, text="Available:", items=leftstart)
        self.leftbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        midfrm = tk.Frame(self)
        midfrm.pack(side=tk.LEFT)
        btn = ttk.Button(midfrm, text="\n>\n", width=2, command=self.on_moveright)
        btn.pack()
        btn = ttk.Button(midfrm, text="\n<\n", width=2, command=self.on_moveleft)
        btn.pack()

        self.rightbox = SortableListbox(self, text="Selected:", items=rightstart)
        self.rightbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_moveright(self):
        if (item := self.leftbox.popcurrent()):
            self.rightbox.append(item)

    def on_moveleft(self):
        if (item := self.rightbox.popcurrent()):
            self.leftbox.append(item)

    def loadnew(self, items):
        # clear the left box
        # load the given items into left box if they are not already in the right box
        leftitems = []
        rightitems = self.rightbox.items
        for item in items:
            if item not in rightitems:
                leftitems.append(item)
        self.leftbox.replace(leftitems)

def test():
    r = tk.Tk()
    options = "Red Delicious,Golden Delicious,Granny Smith,Fuji,Gala,Honeycrisp,Braeburn,Pink Lady,McIntosh".split(",")
    columns = OptionsSelect(text="Select column headers", leftstart=options)
    columns.pack(fill=tk.BOTH, expand=True)
    r.mainloop()

if __name__ == "__main__":
    test()
