import tkinter as tk
from tkinter import ttk  # ttk is the modern tk
import customtkinter as ctk
from styleConf import radio_conf
# inputs is defined as an array


class panel_maker:
    def __init__(self, control_panel):
        self.control_panel = control_panel

    # contains:
    # file name
    # embedding?
    # embedding size
    # training data size
    def makestart(self):
        panel = tk.PanedWindow(
            self.control_panel, orient=tk.HORIZONTAL, background="#2c2c2c")
        ex = tk.IntVar(value=1)
        filename = tk.StringVar()

        label = tk.Label(panel, text="start menu")
        test = ctk.CTkRadioButton(panel, text="test", variable=ex, value=1)
        run = ctk.CTkRadioButton(panel, text="run", variable=ex, value=2)
        custom = ctk.CTkRadioButton(panel, text="custom", variable=ex, value=3)
        entry = tk.Entry(panel, textvariable=filename)
        entry2 = tk.Entry(panel, textvariable=filename)

        radio_conf(test)
        radio_conf(run)
        radio_conf(custom)

        panel.add(label)
        panel.add(test)
        panel.add(run)
        # panel.add(custom)
        panel.add(entry)

        sp = startpanel(panel, label, entry)
        sp.execute = ex
        sp.filename = filename
        return sp

    def makelin(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        width = tk.IntVar(value=8)

        label = tk.Label(panel, text="lin menu")
        spinbox = tk.Spinbox(panel, from_=0, to=1024, textvariable=width)
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(spinbox)
        # panel.add(entry)

        lp = linpanel(panel, label, spinbox, entry)
        lp.width = width
        return lp

    def makebatch(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        batch = tk.IntVar(value=4)
        block = tk.IntVar(value=8)
        v = tk.IntVar(value=1)

        label = tk.Label(panel, text="batch menu")
        spinboxa = tk.Spinbox(panel, from_=0, to=1024, textvariable=batch)
        spinboxb = tk.Spinbox(panel, from_=0, to=1024, textvariable=block)

        # train and validate
        train = tk.Radiobutton(panel, text="train", variable=v, value=1)
        validate = tk.Radiobutton(panel, text="validate", variable=v, value=2)

        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(spinboxa)
        panel.add(spinboxb)
        panel.add(train)
        panel.add(validate)
        # panel.add(entry)

        bp = batchpanel(panel, label, spinboxa, spinboxb, entry)
        bp.batch = batch
        bp.block = block
        bp.split = v
        return bp

    def makeembs(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        embs = tk.IntVar(value=8)

        label = tk.Label(panel, text="emb menu")
        spinboxa = tk.Spinbox(panel, from_=0, to=1024, textvariable=embs)
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(spinboxa)
        # panel.add(entry)

        bp = embpanel(panel, label, spinboxa)
        bp.embs = embs
        return bp

    def makemult(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)

        a = tk.IntVar(value=1)
        b = tk.IntVar(value=0)
        flip = tk.IntVar(value=0)

        label = tk.Label(panel, text="multiplication menu")
        checkboxa = tk.Checkbutton(
            panel, text="transposea", variable=a, onvalue=1, offvalue=0)
        checkboxb = tk.Checkbutton(
            panel, text="transposeb", variable=b, onvalue=1, offvalue=0)
        checkboxc = tk.Checkbutton(
            panel, text="flip", variable=flip, onvalue=1, offvalue=0)

        panel.add(label)
        panel.add(checkboxa)
        panel.add(checkboxb)
        panel.add(checkboxc)

        mp = multpanel(panel, label, checkboxa, checkboxb)
        mp.transposea = a
        mp.transposeb = b
        mp.flip = flip

        return mp

    def makescript(self, filesave):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        filename = tk.StringVar(value="filename")
        prog = tk.StringVar(value="# set to default")

        label = tk.Label(panel, text="script menu")
        button = ttk.Button(
            panel, text="filesave", command=filesave
        )
        entrya = tk.Entry(panel, textvariable=filename)
        entryb = tk.Entry(panel, textvariable=prog)

        panel.add(label)
        # panel.add(button)
        # panel.add(entrya)
        panel.add(entryb)

        sp = scriptpanel(panel, label, button, entrya, entryb)
        sp.filename = filename
        sp.prog = prog

        return sp

    def makesplit(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        fraction = tk.IntVar(value=4)
        offset = tk.IntVar(value=4)

        label = tk.Label(panel, text="split menu")
        spinboxa = tk.Spinbox(panel, from_=1, to=32, textvariable=fraction)
        spinboxb = tk.Spinbox(panel, from_=1, to=32, textvariable=offset)

        panel.add(label)
        panel.add(spinboxa)
        panel.add(spinboxb)

        sp = splitpanel(panel, label, spinboxa, spinboxb)
        sp.fraction = fraction
        sp.block = offset
        return sp

    def makedrop(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        drop = tk.IntVar(value=0)

        label = tk.Label(panel, text="split menu")
        spinbox = tk.Spinbox(
            panel, from_=0, to=0.95, increment=0.05, textvariable=drop)

        panel.add(label)
        panel.add(spinbox)

        dp = droppanel(panel, label, spinbox)
        dp.drop = drop

        return dp

    def makeempty(self, menuname):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        label = tk.Label(panel, text=f"{menuname} menu")

        panel.add(label)

        ep = emptypanel(panel, label)
        return ep


class emptypanel:
    def __init__(self, panel, label):
        self.panel = panel
        self.label = label


class droppanel:
    def __init__(self, panel, label, spinbox):
        self.panel = panel
        self.label = label
        self.spinbox = spinbox

        self.drop = None


class splitpanel:
    def __init__(self, panel, label, spinboxa, spinboxb):
        self.panel = panel
        self.label = label
        self.spinboxa = spinboxa
        self.spinboxb = spinboxb

        self.fraction = None
        self.block = None


class scriptpanel:
    def __init__(self, panel, label, button, entrya, entryb):
        self.panel = panel
        self.label = label
        self.button = button
        self.entrya = entrya
        self.entryb = entryb

        self.filename = None
        self.prog = None


class multpanel:
    def __init__(self, panel, label, checkboxa, checkboxb):
        self.panel = panel
        self.label = label
        self.checkboxa = checkboxa
        self.checkboxb = checkboxb

        self.transposea = None
        self.transposeb = None
        self.flip = None


class embpanel:
    def __init__(self, panel, label, spinboxa):
        self.panel = panel
        self.label = label
        self.spinbox = spinboxa

        self.embs = None


class batchpanel:
    def __init__(self, panel, label, spinboxa, spinboxb, entry):
        self.panel = panel
        self.label = label
        self.spinboxa = spinboxa
        self.spinboxb = spinboxb
        self.entry = entry

        self.batch = None
        self.block = None
        self.split = None


class linpanel:
    def __init__(self, panel, label, spinbox, entry):
        self.panel = panel
        self.label = label
        self.spinbox = spinbox
        self.entry = entry

        self.width = None


class startpanel:
    def __init__(self, panel, label, entry):
        self.panel = panel
        self.label = label
        self.entry = entry

        self.execute = None
        self.filename = None
