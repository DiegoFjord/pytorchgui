import tkinter as tk
import json
# my imports
from control import control
from items import nnCustom
from screenItems import screenItems
from winInit import winInit

# my imports


# root
root = tk.Tk()
root.title("title")
root.geometry("750x750")


def set_focus(e):
    e.widget.focus_set()

# function handlers


def clear_session():
    # Loop through all widgets inside the root window
    for widget in root.winfo_children():
        widget.destroy()


def load_session():
    # holds items
    _ = winInit(root)


load_session()

root.bind('<Button-1>', set_focus)
# grab items
root.mainloop()
