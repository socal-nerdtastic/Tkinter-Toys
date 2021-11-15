#!/usr/bin/env python3
#

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import re

bullet = re.compile(r'[\*]+\ ')
BULLET_SEP = ' '

class BulletList(ScrolledText):
    """ Features:
      - pressing Tab on a blank line starts a 'list' by inserting a bullet '* '
      - pressing Tab after a list bullet will add another one, so '* ' goes to '** '
      - pressing Shift-Tab after a list bullet will add another one, so '** ' goes to '* '
      - pressing Enter after a list bullet when nothing else is on the line will remove the bullet
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Return>', self.make_list)
        self.bind('<Tab>', self.indent_list)

    def indent_list(self, event=None):
        """ on TAB """
        line = self.get('insert linestart', 'insert')
        if (m := bullet.match(line)):
            bullets, _, remainder = line.partition(BULLET_SEP)
            if remainder.strip():
                return # not at insert point
            self.delete('insert linestart', 'insert')
            if event.state & 1:
                self.insert('insert', f"{bullets[:-1]} ") # dedent
            else:
                self.insert('insert', f"{bullets}{bullets[-1]} ") # indent
            return "break"
        elif line == '':
            self.insert('insert', "* ") # indent
            return "break"

    def make_list(self, event=None):
        """ on RETURN """
        line = self.get('insert linestart', 'insert lineend')
        if (m := bullet.match(line)):
            bullets, _, remainder = line.partition(BULLET_SEP)
            if remainder.strip():
                # make new bullet point if data was on this line
                self.after(10, self.insert, tk.INSERT, m.group())
            else:
                # end list if no new data (double return)
                self.delete('insert linestart', 'insert lineend')

def main():
    root = tk.Tk()
    win = BulletList(root)
    win.insert('1.0', demo_data)
    win.pack()
    root.mainloop()

demo_data = '''
Some header
* point one
* point two
** subpoint one

another list
* point A
* point B
'''

if __name__ == "__main__":
    main()
