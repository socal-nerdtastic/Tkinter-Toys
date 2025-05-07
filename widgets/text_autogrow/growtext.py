
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class GrowTextMixin:
    """A Text widget that will grow or shrink vertically depending on the content
    setting the height will limit the growth"""
    def __init__(self, parent=None, **kwargs):
        self.lines = 2
        self.maxlines = kwargs.pop("height", None)
        super().__init__(parent, height=self.lines, **kwargs)
        self.bind('<<Modified>>', lambda e: self.after(50, self.on_change)) # limit updates to once every 50 ms.
    def on_change(self, event=None):
        if self.edit_modified():
            lines = int(float(self.index(tk.END)))
            if lines != self.lines and not (self.maxlines and lines > self.maxlines):
                self.lines = lines
                self.config(height=lines)
            self.edit_modified(False)

class GrowText(GrowTextMixin, tk.Text):
    pass
class GrowScrolledText(GrowTextMixin, ScrolledText):
    pass

##DEMO
def demo():
    r = tk.Tk()
    g = GrowText(width=40)
    g.insert(tk.END, "type some lines of text.\n")
    g.insert(tk.END, "Text will expand forever!")
    g.pack(fill=tk.X, expand=True)
    g.focus()

    g = GrowScrolledText(width=40, height=5)
    g.insert(tk.END, "Up to 5 lines of text allowed here.\n")
    g.insert(tk.END, "And then the scrollbar takes over.")
    g.pack(fill=tk.X, expand=True)
    r.mainloop()

if __name__ == "__main__":
    demo()
