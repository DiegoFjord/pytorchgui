import json
import tkinter as tk
# my imports
from winInit import winInit

# my imports


# root
root = tk.Tk()
root.title("title")
root.geometry("1200x800")


def set_focus(e):
    e.widget.focus_set()


def load_appstate():
    with open("App.json", 'r', encoding="utf-8") as f:
        text = f.read()
    return json.loads(text)


# function handlers
def load_session():
    # holds items
    state = load_appstate()
    winInit(root, state)


load_session()

root.bind('<Button-1>', set_focus)
# grab items
root.mainloop()
