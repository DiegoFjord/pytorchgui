import tkinter as tk
from tkinter import ttk  # ttk is the modern tk
import random


class designer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.shapedict = {}

    def move(self, shape_id, dx, dy):
        # FIX: id
        for shape_id in self.shapedict[shape_id].shape_id_arr:
            self.canvas.move(shape_id, dx, dy)

    def getbystring(self, nntype):
        cs = None
        match nntype:
            case "Start": cs = canvasNone(self.canvas)
            case "Batch": cs = canvasNone(self.canvas)
            case "Embeddings": cs = canvasNone(self.canvas)
            case "Linear": cs = canvasNone(self.canvas)
            case "Script": cs = canvasNone(self.canvas)
            case "Custom": cs = canvasNone(self.canvas)
            case _:
                cs = canvasNone(self.canvas)
                print("designer: item not found")
        self.shapedict[cs.head_id] = cs
        return cs.head_id


class canvasBatch:
    def __init__(self, canvas: tk.Canvas):
        self.head_id = canvas.create_rectangle(
            0, 0, 100, 100,
            fill="red",
            outline=""
        )
        self.shape_id_arr = []


class canvasStart:
    def __init__(self, canvas: tk.Canvas):
        self.head_id = canvas.create_rectangle(
            0, 0, 100, 100,
            fill="pink",
            outline=""
        )
        self.shape_id_arr = []

        for a in range(0, 6):
            for b in range(0, 6):
                x = a * 16 + 5
                y = b * 16 + 5
                shape_id = canvas.create_oval(
                    x, y, x+10, y+10, fill="orange", outline=""
                )
                self.shape_id_arr.append(shape_id)


class canvasNone:
    def __init__(self, canvas: tk.Canvas):
        self.head_id = canvas.create_rectangle(
            0, 0, 100, 100,
            fill="red",
            outline=""
        )
        self.shape_id_arr = []
