# this is a comment
from control import nnItem
from items import nnStart, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril, nnDropout


class nndeserial:
    def __init__(self, my_nn_maker):
        self.my_nn_maker = my_nn_maker

    def deserialize(self, item_json):
        print("running deserialize")
        my_nnItem: nnItem = self.my_nn_maker.make_nnItem(item_json["type"])

        # # FIX: start doesnt run becuase of nnMaker
        # if my_nnItem is None:
        #     return None
        #

        panel = my_nnItem.curr.nn_panel

        match my_nnItem.nntype:
            case "Start":
                panel.filename.set(item_json["filename"])
            case "Linear":
                panel.width.set(item_json["width"])
            case "Batch":
                panel.split.set(item_json["split"])
            case "Embeddings":
                panel.embs.set(item_json["embs"])
            case "Multiply":
                panel.transposea.set(item_json["transposea"])
                panel.transposeb.set(item_json["transposeb"])
            case "Script":
                panel.filename.set(item_json["filename"])
                panel.prog.set(item_json["prog"])
            case "Dropout":
                panel.spinvar.set(item_json["dropout"])
            case "Split":
                panel.fraction.set(item_json["fraction"])
                panel.fraction.set(item_json["block"])
            case "Tril": pass
        return my_nnItem


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
