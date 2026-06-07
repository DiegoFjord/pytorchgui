# import array as arr
import tkinter as tk
from items import nnStart
# from torch.nn import functional as F


class nnItem:
    def __init__(self, curr, nnType):
        self.nntype = nnType
        self.curr = curr
        self.nexts = []
        self.prevs = []

        self.line_nexts = []
        self.line_prevs = []

    # this is something
    def call(self, prev):
        # FIX: account for looping (might not be an issue?)
        result = self.curr.run(prev)
        for item in self.nexts:
            # item.run(result)
            item.call(result)


class control:
    def __init__(self, root):
        # NOTE: tree stuff
        self.treeStart = None
        self.itemset = {}

        # NOTE: file stuff
    def run(self):
        self.treeStart.call("passed")
