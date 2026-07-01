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
    def __init__(self, root, state, filename=None):
        self.root = root
        self.state = state
        self.toggle = True
        # self.state = state

        self.winframe = tk.Frame(root)
        self.winframe.pack(fill="both", expand=True)
        winframe = self.winframe

        framea = tk.Frame(winframe)
        frameb = tk.Frame(winframe)
        framec = tk.Frame(winframe)

        self.initApp(frameb, framec, filename)
        self.tkinterObjects(framea)
        self.renderwin(framea, frameb, framec)

    def __del__(self):
        with open("App.json", 'w', encoding="utf-8") as f:
            jsonstring = json.dumps(self.state)
            f.write(jsonstring)

    def reset(self, filename=None):
        self.winframe.destroy()
        self.__init__(self.root, self.state, filename)

    def initApp(self, frameb, framec, filename=None):
        # holds items
        self.controller = control()
        # creates item panels
        my_panel_maker = panel_maker(frameb)
        # ddCanvas
        self.canvas = tk.Canvas(framec, width=400, height=400, bg="white")
        self.ddCanvas = DragDropCanvas(self.canvas, self.controller)
        # creates items
        self.my_nn_maker = nnMaker(
            my_panel_maker, self.controller, self.ddCanvas)
        # controller
        self.controller.treeStart = self.my_nn_maker.make_nnItem("Start")
        # file save/load
        self.handler = handlefile(self.controller, self.my_nn_maker, filename)
        # create/render items

    def tkinterObjects(self, framea):
        # object options
        options1 = [
            "Linear", "Batch", "Embeddings",
            "Multiply", "Script", "Split", "Line",
            "Tril", "Dropout", "Terminate", "Dropout",
            "LayerNorm", "Relu"
        ]
        options2 = self.state["libs"]
        options3 = ["a", "b", "c"]
        # create objects
        appLabel = tk.Label(framea, text="PytorchGui")
        appLabel.pack()

        # combo boxes
        combo_frame = tk.Frame(framea)
        combo_frame.pack(fill="both", expand=True)

        self.nn_combo = ttk.Combobox(
            combo_frame, values=options1, state="readonly")
        self.custom_combo = ttk.Combobox(
            combo_frame, values=options2, state="readonly")

        # control buttons
        button_frame = tk.Frame(framea)
        button_frame.pack(fill="both", expand=True)

        self.start_button = ttk.Button(
            button_frame, text="Run", command=self.controller.run)

        self.mouse_button = ttk.Button(
            button_frame, text="Drag", command=self.setmouse)

        self.reset_button = ttk.Button(
            button_frame, text="reset", command=self.reset)

        self.files_button = ttk.Button(
            button_frame, text="file", command=self.file_objs)

        # file drops
        self.file_frame = tk.Frame(framea)
        file_frame = self.file_frame

        self.save_as_button = ttk.Button(
            file_frame, text="save to", command=self.save_as)
        self.save_entry = tk.Entry(file_frame)

        self.load_button = ttk.Button(
            file_frame, text="load file", command=self.load)
        self.load_entry = tk.Entry(file_frame)

        self.load_custom_button = ttk.Button(
            file_frame, text="add lib", command=self.load_custom)
        self.custom_entry = tk.Entry(file_frame)

        # handle objects
        self.nn_combo.bind("<<ComboboxSelected>>", self.make_nnItem)
        self.custom_combo.bind("<<ComboboxSelected>>", self.make_customItem)

    def file_objs(self):
        if (self.toggle):
            self.file_frame.pack(fill="both", expand=True)
        else:
            self.file_frame.pack_forget()
        self.toggle = not self.toggle

    def renderwin(self, framea, frameb, framec):
        # render objects
        framea.pack(fill="both", expand=True)
        frameb.pack(fill="both", expand=True)
        framec.pack(fill="both", expand=True)

        # frame a
        self.nn_combo.grid(row=0, column=0)
        self.custom_combo.grid(row=0, column=1)

        self.start_button.grid(row=0, column=0)
        self.mouse_button.grid(row=0, column=1)
        self.reset_button.grid(row=0, column=2)
        self.files_button.grid(row=0, column=3)

        self.save_as_button.grid(row=0, column=0)
        self.save_entry.grid(row=0, column=1)
        self.load_button.grid(row=1, column=0)
        self.load_entry.grid(row=1, column=1)
        self.load_custom_button.grid(row=2, column=0)
        self.custom_entry.grid(row=2, column=1)

        # frame b

        # frame c
        self.ddCanvas.canvas.pack(fill=tk.BOTH, expand=False)

    def setmouse(self):
        self.ddCanvas.state = "Mouse"

    def save_as(self):
        self.handler.filename = self.save_entry.get()
        self.handler.save()

    def save(self):
        if (self.filename):
            self.handler.save()

    def load(self):
        self.reset(self.load_entry.get())

    def make_nnItem(self, out):
        selection = self.nn_combo.get()
        _ = self.my_nn_maker.make_nnItem(selection)

    def load_custom(self):
        customname = self.custom_entry.get()
        opts = list(self.custom_combo['values'])
        opts.append(customname)
        self.custom_combo['values'] = opts
        self.state["libs"].append(customname)

    def checklibjson(self, jsondata):
        follow = jsondata["followdict"]
        itemlist = jsondata["itemlist"]
        for key, value in follow.items():
            mynn = itemlist[int(key)]
            if (len(value) == 0 and mynn["type"] != "Terminate"):
                return False
        return True

    def make_customItem(self, out):
        print("making custom")
        selection = self.custom_combo.get()
        filename = selection
        #
        with open(filename + ".json", "r", encoding="utf-8") as f:
            text = f.read()

        jsondata = json.loads(text)

        if (self.checklibjson(jsondata)):
            custom = self.my_nn_maker.make_nnItem("Custom")
            custom.curr.filename = filename
            print("custom filename: ", custom.curr.filename)
        else:
            print("not valid input")
