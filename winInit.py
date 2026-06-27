import tkinter as tk
import json
# my imports
from canvas import DragDropCanvas
from control import control
from tkinter import ttk  # ttk is the modern tk
from panel_maker import panel_maker
from handlefile import handlefile
from nnMaker import nnMaker


# this is a comment
class winInit:
    def __init__(self, root, filename=None):
        self.root = root

        self.winframe = tk.Frame(root)
        self.winframe.pack(fill="both", expand=True)

        self.initApp(self.winframe, filename)
        self.tkinterObjects(self.winframe)
        self.renderwin()

    def reset(self, filename=None):
        self.winframe.destroy()
        self.__init__(self.root, filename)

    def initApp(self, winframe, filename=None):
        # holds items
        self.controller = control()
        # holds selected item panel
        self.control_panel = ttk.PanedWindow(
            winframe, orient=tk.HORIZONTAL, height=50)
        # creates item panels
        self.my_panel_maker = panel_maker(self.control_panel)
        # ddCanvas
        self.canvas = tk.Canvas(winframe, width=400, height=400, bg="white")
        self.ddCanvas = DragDropCanvas(self.canvas, self.controller)
        # creates items
        self.my_nn_maker = nnMaker(
            self.my_panel_maker, self.controller, self.ddCanvas)
        # controlloer
        self.controller.treeStart = self.my_nn_maker.make_nnItem("Start")
        # file save/load
        self.handler = handlefile(self.controller, self.my_nn_maker, filename)
        # create/render items

    def tkinterObjects(self, winframe):
        # object options
        options1 = [
            "Linear", "Batch", "Embeddings",
            "Multiply", "Script", "Split", "Line",
            "Tril", "Dropout", "Terminate"
        ]
        options2 = [
            "lib1.json"
        ]

        # create objects
        self.label2 = tk.Label(
            winframe, text="Please make a selection", font=("Arial", 12)
        )

        self.combo1 = ttk.Combobox(winframe, values=options1, state="readonly")
        self.combo2 = ttk.Combobox(winframe, values=options2, state="readonly")

        self.start_button = ttk.Button(
            winframe, text="Start Progress", command=self.controller.run
        )

        self.mouse_button = ttk.Button(
            winframe, text="set mouse", command=self.setmouse)
        self.save_button = ttk.Button(
            winframe, text="save", command=self.save)
        self.save_entry = tk.Entry(winframe)
        self.load_button = ttk.Button(
            winframe, text="load", command=self.load)
        self.load_entry = tk.Entry(winframe)
        self.reset_button = ttk.Button(
            winframe, text="reset", command=self.reset)

        label = tk.Label(winframe, text="App")
        self.control_panel.add(label)

        # handle objects
        self.combo1.bind("<<ComboboxSelected>>", self.make_nnItem)
        self.combo2.bind("<<ComboboxSelected>>", self.make_customItem)

    def renderwin(self):
        # render objects
        self.label2.pack(pady=20)
        self.combo1.pack(pady=5)
        self.combo2.pack(pady=5)
        self.start_button.pack(pady=10)
        self.mouse_button.pack(pady=10)
        self.save_button.pack(pady=5)
        self.save_entry.pack(pady=5)
        self.load_button.pack(pady=5)
        self.load_entry.pack(pady=5)
        self.reset_button.pack(pady=5)
        self.control_panel.pack(fill=tk.Y, expand=False)
        self.ddCanvas.canvas.pack(fill=tk.BOTH, expand=False)

    def setmouse(self):
        self.ddCanvas.state = "Mouse"

    def save(self):
        self.handler.filename = self.save_entry.get()
        self.handler.save()

    def load(self):
        self.reset(self.load_entry.get())

    def make_nnItem(self, out):
        selection = self.combo1.get()
        _ = self.my_nn_maker.make_nnItem(selection)

    def checklibjson(jsondata):
        follow = jsondata["followdict"]
        itemlist = jsondata["itemlist"]
        for key, value in follow.items():
            mynn = itemlist[int(key)]
            if (len(value) == 0 and mynn["type"] != "Terminate"):
                return False
        return True

    def make_customItem(self, out):
        selection = self.combo2.get()
        filename = str(selection) + ".json"
        #
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        jsondata = json.loads(text)

        if (self.checklibjson(jsondata)):
            custom = self.my_nn_maker.make_nnItem("Custom")
            custom.filename = filename
        else:
            print("not valid input")
