
class nnItem:
    def __init__(self, curr, nnType):
        self.nntype = nnType
        self.curr = curr
        self.nexts = []
        self.prevs = []

        # TODO: make into a dictionary and place in canvas
        # item: line_id
        self.line_nexts = []
        self.line_prevs = []

    def call(self, prev):
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

        for item in self.itemlist:
            item.curr.setup = True

    def load_vals(self):
        for item in self.itemlist:
            item.curr.get_user_data()

    def remove_item(self, item: nnItem, item_id):
        for prev_item in item.prevs:
            prev_item.nexts.remove(item)
            for line_next in prev_item.line_nexts:
                for line_prev in item.line_prevs:
                    if (line_next == line_prev):
                        prev_item.line_nexts.remove(line_next)
                        print("removing next line")

        for next_item in item.nexts:
            next_item.prevs.remove(item)
            for line_prev in next_item.line_prevs:
                for line_next in item.line_nexts:
                    if (line_prev == line_next):
                        next_item.line_prevs.remove(line_prev)
                        print("removing prev line")

        self.itemset.pop(item_id)
