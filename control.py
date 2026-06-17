import json
from items import nnStart, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril, nnDropout


class nnItem:
    def __init__(self, curr, nnType):
        self.nntype = nnType
        self.curr = curr
        self.nexts = []
        self.prevs = []  # could make into static number?

        self.line_nexts = []
        self.line_prevs = []

    def call(self, prev):
        # FIX: account for looping (might not be an issue?)
        # if result is None break
        result = self.curr.run(prev)
        for item in self.nexts:
            item.call(result)


class control:
    def __init__(self, root):
        # NOTE: tree stuff
        self.treeStart = None
        self.itemset = {}

        # NOTE: file stuff
    def run(self):
        self.treeStart.call("passed")

        for key, value in self.itemset.items():
            value.curr.setup = True

    def save(self):
        serial = nnserial()
        jsondata = {}

        indexdict = {self.treeStart: 0}
        itemlist = [self.treeStart]
        followdict = {}

        # add items to list
        # add items to nnitem:index dictionary

        i = 1
        for key, value in self.itemset.items():
            itemlist.append(value)
            indexdict[value] = i
            i += 1

        # add nexts
        for index, item in enumerate(itemlist):
            nextlist = []

            for nextitem in item.nexts:
                nextlist.append(indexdict[nextitem])

            followdict[index] = nextlist

        # make itemlist for serialization
        for index, item in enumerate(itemlist):
            itemlist[index] = serial.serialize(item)

        print("itemlist", itemlist)


class nnserial:
    def __init__(self):
        pass

    def serialize(self, item: nnItem):
        match item.nntype:
            case "Start": return self.start(item)
            case "Linear": return self.linear(item)
            case "Batch": return self.batch(item)
            case "Embeddings": return self.emb(item)
            case "Multiply": return self.mult(item)
            case "Script": return self.script(item)
            case "Dropout": return self.script(item)
            case "Split": return self.split(item)
            case "Tril": return self.tril(item)

    def start(self, item: nnItem):
        start: nnStart = item.curr
        return {item.nntype: {"filename": start.filename}}

    def linear(self, item: nnItem):
        lin: nnLinear = item.curr
        return {item.nntype: {"width": lin.width}}

    def batch(self, item: nnItem):
        batch: nnBatch = item.curr
        return {item.nntype: {"split": batch.split}}

    def emb(self, item: nnItem):
        # emb: nnEmbedings = item.curr
        return {item.nntype: None}

    def mult(self, item: nnItem):
        mult: nnMultiply = item.curr
        return {item.nntype: {
            "transposea": mult.transposea, "transposeb": mult.transposeb
        }}

    def script(self, item: nnItem):
        script: nnScript = item.curr
        return {item.nntype: {"filename": script.exec_file}}

    def drop(self, item: nnItem):
        drop: nnDropout = item.curr
        return {item.nntype: {"dropout": drop.drop}}

    def split(self, item: nnItem):
        split: nnSplit = item.curr
        return {item.nntype: {
            "fraction": split.fraction, "block": split.block
        }}

    def tril(self, item: nnItem):
        start: nnTril = item.curr
        return {item.nntype: None}
