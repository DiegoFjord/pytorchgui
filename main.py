import tkinter as tk
# my imports
from canvas import DragDropCanvas
from control import control
from tkinter import ttk  # ttk is the modern tk
from panel_maker import panel_maker
from screenItems import screenItems
from handlefile import handlefile
from nnMaker import nnMaker, basicMaker
from items import nnCustom
# my imports


# root
root = tk.Tk()
root.title("title")
root.geometry("750x750")


# function handlers
def setmouse():
    ddCanvas.state = "Mouse"


def make_nnItem(out):
    selection = item_decl.combo1.get()
    _ = my_nn_maker.make_nnItem(selection)


def make_customItem(out):
    selection = item_decl.combo2.get()
    custom: nnCustom = my_nn_maker.make_nnItem("Custom")
    custom.filename = str(selection) + ".txt"


# holds items
controller = control()
# holds selected item panel
control_panel = ttk.PanedWindow(root, orient=tk.HORIZONTAL, height=50)
# creates item panels
my_panel_maker = panel_maker(control_panel)
# ddCanvas
canvas = tk.Canvas(root, width=400, height=400, bg="white")
ddCanvas = DragDropCanvas(canvas, controller)
# creates items
my_nn_maker = nnMaker(my_panel_maker, controller, ddCanvas)
# controlloer
controller.treeStart = my_nn_maker.make_nnItem("Start")
# file save/load
handler = handlefile(controller, my_nn_maker)
# create/render items
item_decl = screenItems(
    root, controller, handler, ddCanvas, control_panel, setmouse,
    make_nnItem, make_customItem
)
# grab items
root.mainloop()
