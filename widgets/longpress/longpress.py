
import tkinter as tk

class LongPressButton(tk.Button):
    """A button that runs a command repeatidly as long as the button is held down"""
    def __init__(self, master=None, command=None, repeat_time=250, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.repeat_time = repeat_time
        self.command_trigger = ' '
        self.bind('<ButtonPress-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)

    def on_press(self, event=None):
        if self.command is not None:
            self.command()
        self.command_trigger = self.after(self.repeat_time, self.on_press)

    def on_release(self, event=None):
        self.after_cancel(self.command_trigger)

class LongPressKey:
    def __init__(self, key, on_press_command=None, on_release_command=None, widget=None):
        self.on_press_command = on_press_command
        self.on_release_command = on_release_command
        self.pressed = False
        widget = widget or tk._default_root
        widget.bind(f'<KeyPress-{key}>', self.on_press)
        widget.bind(f'<KeyRelease-{key}>', self.on_release)

    def on_press(self, event=None):
        if not self.pressed and self.on_press_command is not None:
            self.on_press_command()
        self.pressed = True

    def on_release(self, event=None):
        if self.on_release_command is not None:
            self.on_release_command()
        self.pressed = False

### TEST / DEMO:
from itertools import cycle

class Spinner(tk.Label):
    def __init__(self, parent=None, text='', **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text
        self.chars = cycle("|/-\\")
        self.timer = ' '
        self.update()
    def update(self):
        self.config(text=f"{self.text}\n{next(self.chars)}")
    def spinning(self):
        self.update()
        self.timer = self.after(100, self.spinning)
    def stop(self):
        self.after_cancel(self.timer)

def main():
    root = tk.Tk()
    leftfrm = tk.Frame(root)
    leftfrm.pack(side=tk.LEFT)
    lbl_spin = Spinner(leftfrm, text='button press:')
    greenbutton = LongPressButton(leftfrm, text='click and hold me!!', bg='green', command=lbl_spin.update)
    greenbutton.pack()
    bluebutton = LongPressButton(leftfrm, text="I'm faster!!", bg='light blue', command=lbl_spin.update, repeat_time=80)
    bluebutton.pack()
    lbl_spin.pack()

    tk.Frame(width=10).pack(side=tk.LEFT)

    rightfrm = tk.Frame(root)
    rightfrm.pack(side=tk.LEFT)
    tk.Label(rightfrm, text="press the 'a' or 'b' key!").pack()

    lbl_a = Spinner(rightfrm, text='"a" key:')
    lbl_a.pack()
    LongPressKey('a', on_press_command=lbl_a.spinning, on_release_command=lbl_a.stop) # set the functions to call on key press and release

    lbl_b = Spinner(rightfrm, text='"b" key:')
    lbl_b.pack()
    LongPressKey('b', lbl_b.spinning, lbl_b.stop)

    root.mainloop()

if __name__ == "__main__":
    main()
