import tkinter as tk

SCROLL_SPEED = 60 # in ms per pixel scrolled
END_PAUSE_TIME = 500 # how long to pause when the end is reached before restarting
class MarqueeLabel:
    """This label cannot set it's own size. You must layout this label
    in a place where the container sets the size"""
    def __init__(self, parent=None, **kwargs):
        self.frm = tk.Frame(parent)
        tk.Label(self.frm, text=" ").pack()
        self.lbl = tk.Label(self.frm, **kwargs)
        self.lbl.place(relx=.5, y=0, anchor='n')
        self.scrolling = False
        tk._default_root.bind("<Configure>", self.scroll_set, "+")
        self.outer_attr = set(dir(tk.Widget))

    def scroll_set(self, event):
        if self.frm.winfo_width() < self.lbl.winfo_width():
            if not self.scrolling:
                self.lbl.place_forget()
                self.lbl.place(x=0, y=0, anchor="nw")
                self.scrolling = True
                self.scroll_loop()

    def scroll_loop(self, x=0):
        if self.frm.winfo_width() > self.lbl.winfo_width():
            self.lbl.place_forget()
            self.lbl.place(relx=.5, y=0, anchor='n')
            self.scrolling = False
        elif -x > (self.lbl.winfo_width()-self.frm.winfo_width()):
            self.lbl.after(END_PAUSE_TIME, self.scroll_loop, 0)
        else:
            self.lbl.place_configure(x=x)
            self.lbl.after(SCROLL_SPEED, self.scroll_loop, x-1)

    def __getattr__(self, item):
        return getattr(self.frm if item in self.outer_attr else self.lbl, item)

## DEMO
def demo():
    root = tk.Tk()
    root.columnconfigure(0,weight=1)
    tk.Label(text="Demo program").grid(sticky='ew')
    label = MarqueeLabel(text="Can anyobody help me make an autoscroll function that achieves this?")
    label.grid(sticky='ew')
    root.mainloop()

if __name__ == "__main__":
    demo()
