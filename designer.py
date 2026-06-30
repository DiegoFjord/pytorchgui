import tkinter as tk
from tkinter import ttk  # ttk is the modern tk
import random


class designer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.shapedict = {}

    def move(self, object_id, dx, dy):
        for shape_id in self.shapedict[object_id].shape_id_arr:
            self.canvas.move(shape_id, dx, dy)

    def delete(self, object_id):
        for shape_id in self.shapedict[object_id].shape_id_arr:
            self.canvas.delete(shape_id)

    def getbystring(self, nntype):
        cs = None
        match nntype:
            case "Start": cs = canvasLin(self.canvas)
            case "Batch": cs = canvasBatch(self.canvas)
            case "Embeddings": cs = canvasEmbs(self.canvas)
            case "Linear": cs = canvasStart(self.canvas)
            case "Script": cs = canvasNone(self.canvas)
            case "Custom": cs = canvasNone(self.canvas)
            case _:
                cs = canvasNone(self.canvas)
                print("designer: item not found")
        self.shapedict[cs.head_id] = cs
        return cs.head_id


class canvasHead:
    def __init__(self, canvas: tk.Canvas):
        self.head_id = canvas.create_rectangle(
            0, 0, 100, 100,
            fill="light blue",
            outline=""
        )


class canvasLin(canvasHead):
    def __init__(self, canvas: tk.Canvas):
        canvasHead.__init__(self, canvas)
        self.shape_id_arr = []

        shape_id = canvas.create_rectangle(
            2, 2, 19.6, 98, fill="orange", outline="")
        self.shape_id_arr.append(shape_id)


class canvasEmbs(canvasHead):
    def __init__(self, canvas: tk.Canvas):
        canvasHead.__init__(self, canvas)
        self.shape_id_arr = []

        shape_id = canvas.create_rectangle(
            2, 2, 19.6, 98, fill="orange", outline="")
        self.shape_id_arr.append(shape_id)

        for a in range(0, 4):
            for b in range(0, 5):
                x = a * 19.6 + 21.6
                y = b * 19.6 + 2
                shape_id = canvas.create_rectangle(
                    x, y, x+17.6, y+17.6, fill="orange", outline="")
                self.shape_id_arr.append(shape_id)


class canvasBatch(canvasHead):
    def __init__(self, canvas: tk.Canvas):
        canvasHead.__init__(self, canvas)
        self.shape_id_arr = []

        for a in range(0, 4):
            x = 5
            y = a * 22.5 + 3
            shape_id = canvas.create_rectangle(
                x, y + 5, x+90, y+22, fill="dark blue", outline=""
            )
            self.shape_id_arr.append(shape_id)


class canvasStart(canvasHead):
    def __init__(self, canvas: tk.Canvas):
        canvasHead.__init__(self, canvas)

        self.shape_id_arr = []

        for a in range(0, 6):
            for b in range(0, 6):
                x = a * 16 + 5
                y = b * 16 + 5
                shape_id = canvas.create_oval(
                    x, y, x+10, y+10, fill="orange", outline=""
                )
                self.shape_id_arr.append(shape_id)


class canvasNone(canvasHead):
    def __init__(self, canvas: tk.Canvas):
        self.shape_id_arr = []
