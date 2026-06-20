# this is a comment
from control import nnItem
from items import nnStart, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril, nnDropout


class nndeserial:
    def __init__(self, my_nn_maker):
        self.my_nn_maker = my_nn_maker

    def deserialize(self, item_json):
        print("running deserialize")
        my_nnItem: nnItem = self.my_nn_maker.make_nnItem(item_json["type"])

        # FIX: start doesnt run becuase of nnMaker
        if my_nnItem is None:
            return None

        panel = my_nnItem.curr.nn_panel

        match my_nnItem.nntype:
            case "Start": self.start(panel, item_json)
            case "Linear": self.linear(panel, item_json)
            case "Batch": self.batch(panel, item_json)
            case "Embeddings": self.emb(panel, item_json)
            case "Multiply": self.mult(panel, item_json)
            case "Script": self.script(panel, item_json)
            case "Dropout": self.script(panel, item_json)
            case "Split": self.split(panel, item_json)
            case "Tril": self.tril(panel, item_json)
        return my_nnItem

    def start(self, panel, item_json):
        panel.filename.set(item_json["filename"])

    def linear(self, panel, item_json):
        panel.width.set(item_json["width"])

    def batch(self, panel, item_json):
        panel.split.set(item_json["split"])

    def emb(self, panel, item_json):
        panel.embs.set(item_json["embs"])

    def mult(self, panel, item_json):
        panel.transposea.set(item_json["transposea"])
        panel.transposeb.set(item_json["transposeb"])

    def script(self, panel, item_json):
        panel.filename.set(item_json["filename"])
        panel.prog.set(item_json["prog"])

    def drop(self, panel, item_json):
        panel.spinvar.set(item_json["dropout"])

    def split(self, panel, item_json):
        panel.fraction.set(item_json["fraction"])
        panel.fraction.set(item_json["block"])

    def tril(self, panel, item_json):
        pass


class nnserial:
    def __init__(self):
        pass

    def serialize(self, my_nnItem: nnItem):
        item = my_nnItem.curr
        retdict = {}
        match my_nnItem.nntype:
            case "Start": retdict = {"filename": item.filename}
            case "Linear": retdict = {"width": item.width}
            case "Batch": retdict = {"split": item.split}
            case "Embeddings": retdict = {"embs": item.embs}
            case "Multiply": retdict = {"transposea": item.transposea, "transposeb": item.transposeb}
            case "Script": retdict = {"filename": item.exec_file, "prog": item.prog}
            case "Dropout": retdict = {"dropout": item.drop}
            case "Split": retdict = {"fraction": item.fraction, "block": item.block}
            case "Tril": retdict = {"type": my_nnItem.nntype}

        retdict["type"] = my_nnItem.nntype
        return retdict
