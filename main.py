import tkinter as tk
# my imports
from canvas import DragDropCanvas
from control import control, nnItem
from tkinter import ttk  # ttk is the modern tk
from panel_maker import panel_maker
from items import nnStart, nnLinear, nnTest

# root
root = tk.Tk()
root.title("title")
root.geometry("750x750")

# function handlers


def update_label(out):
    print(out)
    selection = combo.get()
    item_type = None

    if (selection == "Line"):
        app.state = selection
    else:
        app.state = "Mouse"

    if (selection == "Linear"):
        item_type = nnLinear(my_panel_maker)
        app.add_canvas_item(nnItem(item_type, selection))

    if (selection == "Test"):
        item_type = nnTest(my_panel_maker)
        app.add_canvas_item(nnItem(item_type, selection))


# object options
options = ["Linear", "Relu", "Dropout", "Layernorm", "Mouse", "Line"]

# create objects
control_panel = tk.PanedWindow(root, orient=tk.HORIZONTAL)
my_panel_maker = panel_maker(control_panel)
label = tk.Label(control_panel, text="Hello World!")

controller = control(root)
controller.treeStart = nnItem(nnStart("Filename", my_panel_maker), "Start")

canvas = tk.Canvas(root, width=400, height=400, bg="white")
label = tk.Label(root, text="sumting")
label2 = tk.Label(root, text="Please make a selection", font=("Arial", 12))
combo = ttk.Combobox(root, values=options, state="readonly")
start_button = ttk.Button(root, text="Start Progress", command=controller.run)

# handle objects
combo.bind("<<ComboboxSelected>>", update_label)
app = DragDropCanvas(canvas, controller)
control_panel.add(label)

# render objects
label2.pack(pady=20)
combo.pack(pady=5)
start_button.pack(pady=10)
control_panel.pack(fill=tk.BOTH, expand=True)
app.canvas.pack(fill="both", expand=False)

# set objects
root.mainloop()
