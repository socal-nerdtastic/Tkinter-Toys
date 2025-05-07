
import tkinter as tk
import webbrowser

def on_enter(*eventargs):
    txt.config(cursor="hand2")
def on_leave(*eventargs):
    txt.config(cursor="arrow")
def on_click(*eventargs):
    webbrowser.open("https://learnpython.reddit.com")

root = tk.Tk()

txt = tk.Text(root)
txt.insert("1.0", "Check out the best python help site on the internet!")
txt.tag_add("hyperlink", "1.19", "1.35")
txt.tag_configure("hyperlink", foreground="blue", underline=True)
txt.tag_bind("hyperlink", '<Enter>', on_enter)
txt.tag_bind("hyperlink", '<Leave>', on_leave)
txt.tag_bind("hyperlink", '<1>', on_click)
txt.pack()

root.mainloop()
