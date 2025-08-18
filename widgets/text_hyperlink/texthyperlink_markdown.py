#!/usr/bin/env python3
#
# version 2025-08-18

import webbrowser
from functools import partial
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import re

# syntax: My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
# note! the link text cannot contain [] symbols, and the link text cannot contain () symbols!

# todo: add support for \n in the lines
# todo: add link tooltip (alt text) support
# todo: add support for <bracketlinks>

find_markdown = re.compile(r"\[(.*?)\]\((.*?)\)")
class TextHyperlinkMixin:
    """Add a method to the Text widget to insert a hyperlink"""
    links = 0
    def insert_md_line(self, index:str, text:str):
        """markdown format
        My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
        """
        # https://www.markdownguide.org/basic-syntax/#links
        m = find_markdown.search(text)
        if not m: # no link found
            return self.insert(index, text)
        start = self.index("end-1c" if index.lower() == tk.END else index)
        row, col = start.split(".")
        prefix = text[:m.start()]
        suffix = text[m.end():]
        link_text = m.group(1)
        if '\n' in prefix or '\n' in link_text:
            print("ERROR: md links with newlines not yet supported.")
            return self.insert(index, text)
        link_target = m.group(2)
        link_tooltip = ''
        if '"' in link_target:
            link_target, link_tooltip, _ = link_target.split('"')
        link_text = link_text.strip()
        link_target = link_target.strip()
        link_tooltip = link_tooltip.strip()

        self.insert(start, prefix)
        col = int(col)+len(prefix)
        if link_target == "copy":
            link_command = partial(self.on_click_copy, link_tooltip)
        else:
            link_command = partial(self.on_click_open, link_target)
        self.insert_link(f"{row}.{col}", link_text, link_command, link_tooltip)
        col += len(link_text)
        self.insert_md_line(f"{row}.{col}", suffix)

    def insert_link(self:tk.Text, index:str, text:str, command:callable, tooltip:str=None):
        # currently does not support newlines in the text
        tagname = f"hyperlink{self.__class__.links}"
        self.__class__.links += 1
        self.tag_configure(tagname, foreground="blue", underline=True)
        self.tag_bind(tagname, '<Enter>', self.on_enter)
        self.tag_bind(tagname, '<Leave>', self.on_leave)
        if not callable(command):
            command = partial(self.on_click_open, command)
        self.tag_bind(tagname, '<1>', command)
        start = self.index("end-1c" if index.lower() == tk.END else index)
        self.insert(start, text)
        row, col = start.split(".")
        self.tag_add(tagname, start, f"{row}.{int(col)+len(text)}")
    def on_enter(self:tk.Text, event=None):
        self.config(cursor="hand2")
    def on_leave(self:tk.Text, event=None):
        self.config(cursor="arrow")
    def on_click_open(self, link:str, event=None):
        try:
            if link.startswith("http"):
                webbrowser.open(link)
            else:
                os.startfile(link)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open link\n '{link}'\n\n{e}")
    def on_click_copy(self, link:str, event:tk.Event):
        self.clipboard_clear()
        self.clipboard_append(link)
        message = tk.Label(self, bg="Yellow", text="Copied!")
        message.place(x=event.x, y=event.y, anchor=tk.CENTER)
        self.after(500, message.destroy)

class TextHyperlink(tk.Text, TextHyperlinkMixin):
    pass

class ScrolledTextHyperlink(ScrolledText, TextHyperlinkMixin):
    pass

##DEMO
def demo_func(event=None):
    messagebox.showinfo("Hello world!", "You have run a custom function!")

def demo():
    r = tk.Tk()
    t = ScrolledTextHyperlink() # just like normal Text, but with added magic.

    t.insert(tk.END, "Check out the best ")
    t.insert_link(tk.END, "python help site", "https://learnpython.reddit.com")
    t.insert(tk.END, " on the internet!\n")

    t.insert(tk.END, "Open the ")
    t.insert_link(tk.END, "current working directry", ".")
    t.insert(tk.END, " that this program is using.\n")

    t.insert(tk.END, "Run a ")
    t.insert_link(tk.END, "custom python function", demo_func)
    t.insert(tk.END, " from a click!\n")

    t.insert_md_line(tk.END, 'My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy"). What is yours?\n\n')

    t.insert_md_line(tk.END, 'If you want to copy something [click here](copy "some data in your clipboard"). some other (parenthesized data) goes here.\n\n')

    t.insert_md_line(tk.END, 'multiple links: [click here](copy "some data in your clipboard"), or [click here](copy "more data") goes here.\n\n')

    t.pack(fill=tk.X, expand=True)
    t.focus()
    r.mainloop()

if __name__ == "__main__":
    demo()
