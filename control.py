
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
        if (result is None):
            return
        for item in self.nexts:
            item.call(result)


class control:
    def __init__(self):
        # NOTE: tree stuff
        self.treeStart = None
        # TODO: move this to canvas
        self.itemset = {}
        self.itemlist = []

        # NOTE: file stuff
    def run(self):
        self.treeStart.call("passed")

        for key, value in self.itemset.items():
            value.curr.setup = True

    def load_vals(self):
        for key, value in self.itemset.items():
            value.curr.get_user_data()
