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
        v = tk.IntVar(value=1)

        label = tk.Label(panel, text="start menu")
        test = tk.Radiobutton(panel, text="test", variable=v, value=1)
        run = tk.Radiobutton(panel, text="run", variable=v, value=2)
        custom = tk.Radiobutton(panel, text="custom", variable=v, value=3)
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(test)
        panel.add(run)
        panel.add(custom)
        panel.add(entry)

        sp = startpanel(panel, label, entry)
        sp.execute = v
        return sp

    def makelin(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)
        a = tk.IntVar(value=8)

        label = tk.Label(panel, text="lin menu")
        spinbox = tk.Spinbox(panel, from_=0, to=1024, textvariable=a)
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(spinbox)
        panel.add(entry)

        lp = linpanel(panel, label, spinbox, entry)
        lp.spinvar = a
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
        panel.add(entry)

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

        # train and validate

        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(spinboxa)
        panel.add(entry)

        bp = embpanel(panel, label, spinboxa)
        bp.embs = embs
        return bp

    def makemult(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)

        a = tk.IntVar(value=1)
        b = tk.IntVar(value=0)

        label = tk.Label(panel, text="multiplication menu")
        checkboxa = tk.Checkbutton(
            panel, text="transposea", variable=a, onvalue=1, offvalue=0
        )
        checkboxb = tk.Checkbutton(
            panel, text="transposeb", variable=b, onvalue=1, offvalue=0
        )

        panel.add(label)
        panel.add(checkboxa)
        panel.add(checkboxb)

        mp = multpanel(panel, label, checkboxa, checkboxb)
        mp.transposea = a
        mp.transposeb = b

        return mp


class multpanel:
    def __init__(self, panel, label, checkboxa, checkboxb):
        self.panel = panel
        self.label = label
        self.checkbox = checkboxa
        self.checkbox = checkboxb

        self.transposea = None
        self.transposeb = None


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
    def __init__(self, panel, label, entry):
        self.panel = panel
        self.label = label
        self.entry = entry

        self.execute = None
