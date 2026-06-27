import tkinter as tk
# my imports
from tkinter import ttk  # ttk is the modern tk
# my imports


class screenItems:
    def __init__(self, root, controller, handler, ddCanvas, control_panel, setmouse, make_nnItem, make_customItem, save_lib):
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
        label2 = tk.Label(
            root, text="Please make a selection", font=("Arial", 12)
        )

        self.combo1 = ttk.Combobox(root, values=options1, state="readonly")
        self.combo2 = ttk.Combobox(root, values=options2, state="readonly")

        start_button = ttk.Button(
            root, text="Start Progress", command=controller.run
        )

        mouse_button = ttk.Button(root, text="set mouse", command=setmouse)
        save_button = ttk.Button(root, text="save", command=handler.save)
        load_button = ttk.Button(root, text="load", command=handler.load)
        lib_button = ttk.Button(root, text="lib", command=save_lib)

        label = tk.Label(root, text="App")
        control_panel.add(label)

        # handle objects
        self.combo1.bind("<<ComboboxSelected>>", make_nnItem)
        self.combo2.bind("<<ComboboxSelected>>", make_customItem)

        # render objects
        label2.pack(pady=20)
        self.combo1.pack(pady=5)
        self.combo2.pack(pady=5)
        start_button.pack(pady=10)
        mouse_button.pack(pady=10)
        save_button.pack(pady=5)
        load_button.pack(pady=5)
        lib_button.pack(pady=5)
        control_panel.pack(fill=tk.Y, expand=False)
        ddCanvas.canvas.pack(fill=tk.BOTH, expand=False)

    def make_nnItem(self, out):
        selection = self.combo1.get()
        _ = self.my_nn_maker.make_nnItem(selection)

    def make_customItem(self, out):
        selection = item_decl.combo2.get()
        custom: nnCustom = my_winInit.my_nn_maker.make_nnItem("Custom")
        custom.filename = str(selection) + ".txt"
