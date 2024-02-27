#!/usr/bin/env python3
#

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time

TAG_DONE = "done"
TAG_HIGHLIGHT = "data"
TAG_DONE_FMT = "%Y-%m-%d %H:%M:%S"

class HighlightWords(ScrolledText):
    def __init__(self, master, **kwargs):
        """demo of a widget that colors all words in the wordlist red,
        and marks all lines that start with the date and X in strikeout blue"""
        super().__init__(master, **kwargs)
        self.wordlist = []
        self.tag_configure(TAG_DONE, foreground="#0000FF", overstrike=True)
        self.tag_configure(TAG_HIGHLIGHT, foreground="#ff0000")
        self.bind('<<Modified>>', self.set_color)

    def set_color(self, *args):
        # use a timer to set a trigger max rate
        # this triggers twice for every event ... but I don't feel like fixing that ATM
        self.after(100, self._set_color)

    def _set_color(self):
        self._set_done_tag()

        self.tag_remove(TAG_HIGHLIGHT, "1.0", tk.END)
        for word in self.wordlist:
            self._set_highlight_tag(word, TAG_HIGHLIGHT)

    def _set_highlight_tag(self, pattern, tag, start="1.0", end="end", regexp=False):
        # thanks Bryan Oakley
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def _set_done_tag(self):
        self.tag_remove(TAG_DONE, "1.0", tk.END)
        datalines = self.get("1.0", tk.END).splitlines()
        for i, line in enumerate(datalines,1):
            if line.startswith("X ") and len(line) > 3:
                if line[2] != "(" or ")" not in line:
                    datestr = time.strftime(TAG_DONE_FMT)
                    self.insert(f"{i}.2", f"({datestr})")
                line = self.get(f"{i}.1", f"{i}.1 lineend")
                end = line.index(')') + 2 # one for tcl index, one to not include actual char
                self.tag_add(TAG_DONE, f"{i}.{end}", f"{i}.1 lineend")
        self.edit_modified(False)

class Demo(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.words = tk.StringVar()
        self.words.trace('w', self.update_wordlist)
        words = tk.Entry(self, textvariable=self.words)
        words.pack(fill=tk.X, expand=True)
        words.focus()
        self.txt = HighlightWords(self)
        self.txt.pack(fill=tk.X, expand=True)
        self.txt.insert('1.0', lorem_ipsum)

    def update_wordlist(self, *args):
        self.txt.wordlist = self.words.get().split()
        self.txt.event_generate('<<Modified>>')

def main():
    root = tk.Tk()
    win = Demo(root)
    win.pack()
    root.mainloop()

lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed congue et libero mollis laoreet. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Phasellus nibh est, lacinia eget velit vitae, volutpat vulputate nisl. Mauris convallis congue diam, eu egestas metus vehicula eget. Integer sollicitudin ultricies suscipit. Nullam eget cursus metus. Nunc finibus placerat nunc, vitae elementum magna auctor sit amet. Proin suscipit vehicula cursus.

Duis fringilla mi erat, a fringilla risus aliquet fermentum. Vivamus neque turpis, pulvinar sodales sem in, tempor iaculis dui. Nulla et magna ultrices, condimentum massa a, mattis mauris. Sed et tincidunt libero. Vivamus pretium elit velit, eu tincidunt dolor facilisis vitae. Morbi id nisi lectus. In tristique ante a ex ultrices sodales. Vivamus nec hendrerit mi. Integer vitae felis eu est rutrum fermentum.'''

if __name__ == "__main__":
    main()
