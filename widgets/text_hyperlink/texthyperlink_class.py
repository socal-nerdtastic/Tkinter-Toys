#!/usr/bin/env python3

import webbrowser
from functools import partial
import os
import tkinter as tk

class HyperlinkText(tk.Text):
    """Add a method to the Text widget to insert a hyperlink"""
    links = 0
    def insert_hyperlink(self, index, text, link):
        return self._insert_link(index, text, partial(self.on_click_weblink, link))
    def insert_locallink(self, index, text, link):
        return self._insert_link(index, text, partial(self.on_click_locallink, link))
    def _insert_link(self, index, text, command):
        # currently does not support newlines in the text
        tagname = f"hyperlink{self.__class__.links}"
        self.__class__.links += 1
        self.tag_configure(tagname, foreground="blue", underline=True)
        self.tag_bind(tagname, '<Enter>', self.on_enter)
        self.tag_bind(tagname, '<Leave>', self.on_leave)
        self.tag_bind(tagname, '<1>', command)
        if index.lower() == tk.END:
            start = self.index("end-1c")
        else:
            start = self.index(index)
        self.insert(start, text)
        row, col = start.split(".")
        self.tag_add(tagname, start, f"{row}.{int(col)+len(text)}")
    def on_enter(self, event=None):
        self.config(cursor="hand2")
    def on_leave(self, event=None):
        self.config(cursor="arrow")
    def on_click_weblink(self, link, event=None):
        webbrowser.open(link)
    def on_click_locallink(self, link, event=None):
        os.startfile(link)

##DEMO
def demo():
    r = tk.Tk()
    t = HyperlinkText()
    
    t.insert(tk.END, "Check out the best ")
    t.insert_hyperlink(tk.END, "python help site", "https://learnpython.reddit.com")
    t.insert(tk.END, " on the internet!\n")
    
    t.insert(tk.END, "Open the ")
    t.insert_locallink(tk.END, "current working directry", ".")
    t.insert(tk.END, " that this program is using.\n")
    
    t.pack(fill=tk.X, expand=True)
    t.focus()
    r.mainloop()

if __name__ == "__main__":
    demo()
