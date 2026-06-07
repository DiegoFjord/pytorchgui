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
        radiob = tk.Radiobutton(panel, text="B", variable=v, value=1)
        radioc = tk.Radiobutton(panel, text="C", variable=v, value=1)
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

        label = tk.Label(panel, text="this is the lin menu")
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(entry)

        sp = linpanel(panel, label, entry)
        return sp

    def maketest(self):
        panel = tk.PanedWindow(self.control_panel, orient=tk.HORIZONTAL)

        label = tk.Label(panel, text="this is the test menu")
        entry = tk.Entry(panel)

        panel.add(label)
        panel.add(entry)

        sp = testpanel(panel, label)
        return sp


class testpanel:
    def __init__(self, panel, label, entry):
        self.panel = panel
        self.label = label
        self.entry = entry


class linpanel:
    def __init__(self, panel, label, entry):
        self.panel = panel
        self.label = label
        self.entry = entry


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
