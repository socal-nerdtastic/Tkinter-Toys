#!/usr/bin/env python3

def f(obj):
    """list attributes of an object"""
    print(*(f"{x}: {getattr(obj,x)}" for x in dir(obj) if not x.startswith("_")), sep="\n")

def f(obj):
    """list attributes of an object"""
    for key in dir(obj):
        if not key.startswith("_"):
            value = getattr(obj,key)
            if callable(value) and value.__doc__:
                value = repr(value.__doc__[:60])
                key += " call"
            print(key, ":", value)

def main():
    import tkinter as tk
    f(tk.Text)

if __name__ == "__main__":
    main()
