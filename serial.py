# this is a comment
from control import nnItem


class basicdeserial:
    def deserialize(self, item_json):
        from nnMaker import basicMaker
        my_basic_maker = basicMaker()
        print("running deserialize")
        my_basicItem = my_basic_maker.get_basic_item(
            item_json["type"]
        )
        print("typeback", type(my_basicItem))

        match my_basicItem.typename:
            case "Start": pass
            case "Linear":
                my_basicItem.width = item_json["width"]
            case "Multiply":
                my_basicItem.transposea = item_json["transposea"]
                my_basicItem.transposeb = item_json["transposeb"]
            case "Script":
                my_basicItem.filename = item_json["filename"]
                my_basicItem.prog = item_json["prog"]
            case "Dropout":
                my_basicItem.spinvar = item_json["dropout"]
            case "Split":
                my_basicItem.fraction = item_json["fraction"]
                my_basicItem.fraction = item_json["block"]
            case "Tril": pass
            case _: print("SERIAL Unexpected", my_basicItem.typename)
        return my_basicItem


class nndeserial:
    def __init__(self, my_nn_maker):
        self.my_nn_maker = my_nn_maker

    def deserialize(self, item_json):
        print("running deserialize")
        my_nnItem: nnItem = self.my_nn_maker.make_nnItem(item_json["type"])

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
                panel.flip.set(item_json["flip"])
            case "Script":
                panel.filename.set(item_json["filename"])
                panel.prog.set(item_json["prog"])
            case "Dropout":
                panel.drop.set(item_json["dropout"])
            case "Split":
                panel.fraction.set(item_json["fraction"])
                panel.fraction.set(item_json["block"])
            case "Custom":
                panel.filename = item_json["filename"]
            # LayerNorm, Relu, Terminate
            case _: pass
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
            case "Multiply": retdict = {"transposea": item.transposea, "transposeb": item.transposeb, "flip": item.flip}
            case "Script": retdict = {"filename": item.exec_file, "prog": item.prog}
            case "Dropout": retdict = {"dropout": item.dropval}
            case "Custom": retdict = {"filename": item.filename}
            case "Split": retdict = {"fraction": item.fraction, "block": item.block}
            case "Tril": retdict = {"type": my_nnItem.nntype}

        retdict["type"] = my_nnItem.nntype
        return retdict
