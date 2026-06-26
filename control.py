
class nnItem:
    def __init__(self, curr, nnType):
        self.nntype = nnType
        self.curr = curr
        self.nexts = []
        self.prevs = []  # could make into static number?

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

    def remove_item(self, item: nnItem, line_id):
        for prev_item in item.prevs:
            for next_item in prev_item.nexts:
                if (next_item is item):
                    prev_item.nexts.remove(item)
                    break

        for next_item in item.next:
            for prev_item in next_item.nexts:
                if (prev_item is item):
                    next_item.prevs.remove(item)
                    break

        for prev_item in item.line_prevs:
            for next_item in prev_item.line_nexts:
                if (next_item == line_id):
                    prev_item.line_nexts.remove(line_id)
                    break

        for next_item in item.line_next:
            for prev_item in next_item.line_nexts:
                if (prev_item == line_id):
                    next_item.line_prevs.remove(line_id)
                    break

        self.itemset.remove(item)
