import tkinter as tk

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
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        v = tk.IntVar()

        label = tk.Label(panel, text="this is the start menu")
        radioa = tk.Radiobutton(panel, text="A", variable=v, value=1)
        radiob = tk.Radiobutton(panel, text="B", variable=v, value=2)
        radioc = tk.Radiobutton(panel, text="C", variable=v, value=3)
        spinbox = tk.Spinbox(panel, from_=0, to=10)
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(radioa)
        panel.add(radiob)
        panel.add(radioc)
        panel.add(spinbox)
        panel.add(entry)

        sp = startpanel(panel, label, radioa, radiob, radioc, spinbox, entry)
        sp.radiovar = v
        return sp

    def makelin(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        a = tk.IntVar(value=8)

        label = tk.Label(panel, text="this is the lin menu")
        spinbox = tk.Spinbox(panel, from_=0, to=10, textvariable=a)
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(spinbox)
        panel.add(entry)

        lp = linpanel(panel, label, spinbox, entry)
        lp.spinvar = a
        return lp

    def makebatch(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        batch = tk.IntVar(value=8)
        block = tk.IntVar(value=8)
        v = tk.IntVar()

        label = tk.Label(panel, text="this is the batch menu")
        spinboxa = tk.Spinbox(panel, from_=0, to=10, textvariable=batch)
        spinboxb = tk.Spinbox(panel, from_=0, to=10, textvariable=block)

        # train and validate
        train = tk.Radiobutton(panel, text="trian", variable=v, value=1)
        validate = tk.Radiobutton(panel, text="validate", variable=v, value=2)

        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(spinboxa)
        panel.add(spinboxb)
        panel.add(train)
        panel.add(validate)
        panel.add(entry)

        bp = batchpanel(panel, label, spinboxa, spinboxb, entry)
        bp.batch = batch
        bp.block = block
        bp.split = v
        return bp


class batchpanel:
    def __init__(self, panel, label, spinboxa, spinboxb, entry):
        self.panel = panel
        self.label = label
        self.spinbox = spinboxa
        self.spinbox = spinboxb
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

        self.spinvar = None


class startpanel:
    def __init__(self, panel, label, radioa, radiob, radioc, spinbox, entry):
        self.panel = panel
        self.radioa = radioa
        self.radiob = radiob
        self.radioc = radioc
        self.label = label
        self.spinbox = spinbox
        self.entry = entry

        self.radiovar = None
