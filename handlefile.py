import json
from serial import nnserial, nndeserial
from items import nnGlobals
# this is a comment


class handlefile:
    def __init__(self, controller, my_nn_maker, filename):
        self.controller = controller
        self.my_nn_maker = my_nn_maker
        self.filename = filename
        if (filename is not None):
            self.load()

    # NOTE: exta start Fine
    # loads in new file
    def load(self):
        deserializer: nndeserial = nndeserial(self.my_nn_maker)
        with open("saves/" + self.filename + ".json", "r", encoding="utf-8") as f:
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
        panel = self.controller.treeStart.curr.nn_panel
        panel.filename.set(jsonlist[0]["filename"])
        panel.execute.set(jsonlist[0]["execution"])
        for item in jsonlist[1:]:
            temp_item = deserializer.deserialize(item)
            itemlist.append(temp_item)

        # follows
        followdict = json_items["followdict"]
        print(followdict)

        canvas = self.my_nn_maker.ddCanvas
        for index, listitem in enumerate(itemlist):
            canvas.move_by_item(listitem, index * 110, 0)
        for index, listitem in enumerate(itemlist):
            for nn_index in followdict[str(index)]:
                line_id = canvas.get_line()
                canvas.attach_line(
                    listitem,
                    itemlist[nn_index],
                    line_id)

    def save(self):
        jsondata = self.getjson()
        jsonstring = json.dumps(jsondata)

        if self.filename:
            with open("saves/" + self.filename + ".json", "w", encoding="utf-8") as file:
                file.write(jsonstring)

            print("writing json string to file", jsonstring)
        else:
            print("no file found")

    def getjson(self):
        serial = nnserial()

        indexdict = {}
        itemlist = []  # serialize
        followdict = {}  # serialize
        # add items to list
        # add items to nnitem:index dictionary

        for i, value in enumerate(self.controller.itemlist):
            itemlist.append(value)
            indexdict[value] = i
            value.curr.get_user_data()

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

        return jsondata
