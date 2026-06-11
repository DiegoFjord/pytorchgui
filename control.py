class nnItem:
    def __init__(self, curr, nnType):
        self.nntype = nnType
        self.curr = curr
        self.nexts = []
        self.prevs = []

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
