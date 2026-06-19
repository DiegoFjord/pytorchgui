import tkinter as tk
# my imports
from canvas import DragDropCanvas
from control import control, nnItem
from tkinter import ttk  # ttk is the modern tk
from panel_maker import panel_maker
from items import nnGlobals, nnStart, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril
# my imports


class screenItems:
    def __init__(self, root, controller, handler, ddCanvas, control_panel, setmouse, update_label):
        # object options
        options = [
            "Linear", "Batch", "Embeddings",
            "Multiply", "Script", "Split", "Line",
            "Tril"
        ]

        # create objects
        label2 = tk.Label(
            root, text="Please make a selection", font=("Arial", 12)
        )

        self.combo = ttk.Combobox(root, values=options, state="readonly")
        start_button = ttk.Button(
            root, text="Start Progress", command=controller.run
        )

        mouse_button = ttk.Button(root, text="set mouse", command=setmouse)
        save_button = ttk.Button(root, text="save", command=handler.save)
        load_button = ttk.Button(root, text="load", command=handler.load)

        label = tk.Label(root, text="App")
        control_panel.add(label)

        # handle objects
        self.combo.bind("<<ComboboxSelected>>", update_label)

        # render objects
        label2.pack(pady=20)
        self.combo.pack(pady=5)
        start_button.pack(pady=10)
        mouse_button.pack(pady=10)
        save_button.pack(pady=5)
        load_button.pack(pady=5)
        control_panel.pack(fill=tk.Y, expand=False)
        ddCanvas.canvas.pack(fill=tk.BOTH, expand=False)
