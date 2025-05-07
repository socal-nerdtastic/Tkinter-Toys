"""
A demo of the completely undocumented 'uniform' option
This option can keep multiple rows or columns *within the same grid* at the same size

draws a sudoku grid. No game play (yet), this program just makes the graphic
"""

import tkinter as tk

root = tk.Tk()
root.geometry('500x500')
frame = tk.Frame()
frame.pack(expand=True, fill=tk.BOTH)
frame.rowconfigure(list(range(3)), weight=1, uniform='row')
frame.columnconfigure(list(range(3)), weight=1, uniform='col')
lbl_squares = [[] for _ in range(9)]
lbl_rows = [[] for _ in range(9)]
lbl_columns = [[] for _ in range(9)]
for i in range(9):
    row, col = divmod(i, 3)
    subframe = tk.Frame(frame, highlightthickness=1, highlightbackground='gray')
    subframe.grid(row=row, column=col, sticky='nsew')
    subframe.rowconfigure(list(range(3)), weight=1, uniform='subrow')
    subframe.columnconfigure(list(range(3)), weight=1, uniform='subcol')
    for j in range(9):
        subrow, subcol = divmod(j, 3)
        lbl = tk.Label(subframe, font=('', 16), highlightthickness=1, highlightbackground='black')
        lbl.grid(row=subrow, column=subcol, sticky='nsew')
        lbl_squares[i].append(lbl)
        lbl_rows[row*3+subrow].append(lbl)
        lbl_columns[col*3+subcol].append(lbl)

# test code: populate a random square with 8 random digits
import random

# try using lbl_rows or lbl_columns instead of lbl_squares
lbls = random.sample(random.choice(lbl_squares), 8)
digits = random.sample(range(1,10), 8)
for lbl, digit in zip(lbls, digits):
    lbl.config(text=digit)

frame.mainloop()
