import json
from control import nnItem
from serial import nnserial
from items import nnGlobals, nnStart, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril, nnDropout, nnGlobals
# this is a comment


class handlefile:
    def __init__(self, controller, my_nn_maker):
        self.controller = controller
        self.my_nn_maker = my_nn_maker
        self.filename = "savefile.txt"

    # TODO:
    def load(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            text = f.read()

        json_items = json.loads(text)
        itemlist = []

        # set globals
        globalsdict = json_items["globalsdict"]
        nnGlobals.batch_size = globalsdict["batch_size"]
        nnGlobals.block_size = globalsdict["block_size"]
        # create items
        jsonlist = json_items["itemlist"]
        itemlist.append(self.controller.treeStart)
        for item in jsonlist:
            temp_item = self.my_nn_maker.make_nnItem(item["type"])
            if (temp_item is not None):
                itemlist.append(temp_item)

        # follows
        followdict = json_items["followdict"]
        for index, listitem in enumerate(itemlist):
            for nn_index in followdict[str(index)]:
                listitem.nexts.append(itemlist[nn_index])
                itemlist[nn_index].prevs.append(listitem)

        # TODO: add strings

    def save(self):
        serial = nnserial()

        indexdict = {}
        itemlist = []  # serialize
        followdict = {}  # serialize
        # add items to list
        # add items to nnitem:index dictionary

        i = 0
        for key, value in self.controller.itemset.items():
            itemlist.append(value)
            indexdict[value] = i
            value.curr.get_user_data()
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

        globalsdict = {
            "batch_size": nnGlobals.batch_size,
            "block_size": nnGlobals.block_size
        }  # serialze

        jsondata = {
            "globalsdict": globalsdict,
            "itemlist": itemlist,
            "followdict": followdict
        }

        jsonstring = json.dumps(jsondata)

        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(jsonstring)

        print("writing json string to file", jsonstring)
