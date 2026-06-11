import tkinter as tk
# my imports
from canvas import DragDropCanvas
from control import control, nnItem
from tkinter import ttk  # ttk is the modern tk
from panel_maker import panel_maker
from items import nnGlobals, nnStart, nnLinear, nnBatch, nnEmbedings

import torch
import torch_directml
# my imports


# root
root = tk.Tk()
root.title("title")
root.geometry("750x750")

# function handlers


def setmouse():
    app.state = "Mouse"


def update_label(out):
    print(out)
    selection = combo.get()
    item_type = None

    if (selection == "Line"):
        app.state = selection
    else:
        app.state = "Mouse"

    if (selection == "Batch"):
        item_type = nnBatch(my_panel_maker)
        app.add_canvas_item(nnItem(item_type, selection))

    if (selection == "Embeddings"):
        item_type = nnEmbedings(my_panel_maker)
        item_type.to(nnGlobals.device)
        app.add_canvas_item(nnItem(item_type, selection))

    if (selection == "Linear"):
        item_type = nnLinear(my_panel_maker)
        item_type.to(nnGlobals.device)
        app.add_canvas_item(nnItem(item_type, selection))


# object options
options = ["Linear", "Batch", "Embeddings", "Mouse", "Line"]

# create objects
control_panel = ttk.PanedWindow(root, orient=tk.HORIZONTAL, height=50)
my_panel_maker = panel_maker(control_panel)

controller = control(root)
controller.treeStart = nnItem(nnStart("Filename", my_panel_maker), "Start")
canvas = tk.Canvas(root, width=400, height=400, bg="white")

app = DragDropCanvas(canvas, controller)

label = tk.Label(root, text="App")
label2 = tk.Label(root, text="Please make a selection", font=("Arial", 12))
combo = ttk.Combobox(root, values=options, state="readonly")
start_button = ttk.Button(root, text="Start Progress", command=controller.run)
mouse_button = ttk.Button(root, text="set mouse", command=setmouse)

# handle objects
combo.bind("<<ComboboxSelected>>", update_label)
control_panel.add(label)

# render objects
label2.pack(pady=20)
combo.pack(pady=5)
start_button.pack(pady=10)
mouse_button.pack(pady=10)
control_panel.pack(fill=tk.Y, expand=False)
app.canvas.pack(fill=tk.BOTH, expand=False)

# set objects

root.mainloop()
