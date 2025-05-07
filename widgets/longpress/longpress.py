
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

### TEST / DEMO:
def tick_func():
    print("tick")

def main():
    root = tk.Tk()
    root.geometry('200x200')
    greenbutton = LongPressButton(root, text='click and hold me!!', bg='green', command=tick_func)
    greenbutton.pack()
    bluebutton = LongPressButton(root, text="I'm faster!!", bg='light blue', command=tick_func, repeat_time=80)
    bluebutton.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
