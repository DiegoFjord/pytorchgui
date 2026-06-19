# this is a comment
from control import nnItem
from items import nnStart, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril, nnDropout


class nnunserial:
    def __init__(self):
        pass


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
        return {"type": item.nntype, "filename": start.filename}

    def linear(self, item: nnItem):
        lin: nnLinear = item.curr
        return {"type": item.nntype, "width": lin.width}

    def batch(self, item: nnItem):
        batch: nnBatch = item.curr
        return {"type": item.nntype, "split": batch.split}

    def emb(self, item: nnItem):
        emb: nnEmbedings = item.curr
        return {"type": item.nntype, "embs": emb.embs}

    def mult(self, item: nnItem):
        mult: nnMultiply = item.curr
        return {
            "type": item.nntype,
            "transposea": mult.transposea,
            "transposeb": mult.transposeb
        }

    def script(self, item: nnItem):
        script: nnScript = item.curr
        return {"type": item.nntype, "filename": script.exec_file}

    def drop(self, item: nnItem):
        drop: nnDropout = item.curr
        return {"type": item.nntype, "dropout": drop.drop}

    def split(self, item: nnItem):
        split: nnSplit = item.curr
        return {
            "type": item.nntype,
            "fraction": split.fraction,
            "block": split.block
        }

    def tril(self, item: nnItem):
        start: nnTril = item.curr
        return {"type": item.nntype}
