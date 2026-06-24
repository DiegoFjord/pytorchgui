import re
import torch.nn as nn
import torch
import torch_directml
from basicItems import basicDropout, basicLayerNorm, basicLinear, basicMultiply, basicRelu, basicScript, basicSplit, basicTril
import json
from serial import basicdeserial


# global vars
class nnGlobals:
    vocab_size = None
    block_size = None
    batch_size = None
    emb_dims = None
    y = None
    device = torch_directml.device()


class getsetpanel:
    def __init__(self, control_panel):
        # rendering
        self.control_panel = control_panel
        self.nn_panel = None

    def get_user_panel(self):
        self.control_panel.add(self.nn_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.nn_panel.panel)


class nnStart(getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)

        # file
        self.filename = None
        self.execution = None
        self.setup = True

        # rendering
        self.nn_panel = my_panel_maker.makestart()

    def get_user_data(self):
        self.filename = self.nn_panel.filename.get()
        self.execution = self.nn_panel.execute.get()

    def set_user_data(self):
        pass

    def readfile(self):
        # with open(self.filename, 'r', encoding="utf-8") as f:
        # text = f.read()

        text = """this is some, text 1 that is longer than the previous text
           a b c d e f g h i j k l m n o p q r s t u v w x y z
           a b c d e f g h i j k l m n o p q r s t u v w x y z
        """
        # NOTE: tokens
        tokens = re.findall(r"\w+|\s|[^\w\s]", text.lower())

        tokenset = set(tokens)
        tokensetlist = list(tokenset)

        nnGlobals.vocab_size = len(tokensetlist)
        print("vocab size", nnGlobals.vocab_size)

        # TODO: tokenize strings not chars
        stoi = {ch: i for i, ch in enumerate(tokensetlist)}
        itos = {i: ch for i, ch in enumerate(tokensetlist)}

        def encode(s): return [stoi[c] for c in s]
        def decode(b): return ''.join([itos[i] for i in b])

        data = torch.tensor(encode(tokens), dtype=torch.long)
        return data

    def runExecute(self):
        if (self.execution == 1):
            print("\033[33mWarning:\033[0m" + " running test output on start")
            return torch.rand(16, 8, 4).to(nnGlobals.device)
        if (self.execution == 2):
            return self.readfile()
    # this input is a tensor

    def run(self, matrix):
        print("running start")
        if (self.setup):
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        print(self.filename)

        data = self.runExecute()
        # fetch control _panel values on run
        # run other important stuff
        print(data.shape)
        return data


# input starting data
# output training data and holds desired output
# forwards to the nn to train and find loss
class nnBatch(getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)

        self.train_data = None
        self.val_date = None
        self.split = None
        self.setup = True

        self.nn_panel = my_panel_maker.makebatch()

    def parse_data(self, data):
        n = int(1.00*len(data))  # first 90% will be train, rest val
        self.train_data = data[:n]
        self.val_data = data[n:]

    # used for self supervised learning
    # returns a (batch x block) tensor
    def get_batch(self, train_data, val_data, split, batch_size, block_size):
        # generate a small batch of data of inputs x and targets y
        data = train_data if split == 'train' else val_data
        ix = torch.randint(len(data) - block_size, (batch_size,))
        x = torch.stack([data[i:i + block_size] for i in ix])
        y = torch.stack([data[i+1:i + block_size + 1] for i in ix])
        x, y = x.to(nnGlobals.device), y.to(nnGlobals.device)
        nnGlobals.y = y
        return x

    def get_user_data(self):
        nnGlobals.batch_size = self.nn_panel.batch.get()
        nnGlobals.block_size = self.nn_panel.block.get()
        self.split = self.nn_panel.split.get()

    def set_user_data(self):
        if (self.split):
            self.split = "train"
        else:
            self.split = "val"

    def run(self, matrix):
        print("running batch")
        if (self.setup):
            self.get_user_data()
            self.set_user_data()
            self.parse_data(matrix)
            self.setup = False

        x = self.get_batch(
            matrix, matrix, self.split,
            nnGlobals.batch_size, nnGlobals.block_size
        )

        print(x.shape)
        return x


class nnLinear(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        self.lin1 = None
        self.dim = None
        self.width = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makelin()

    def get_user_data(self):
        self.width = self.nn_panel.width.get()

    def set_user_data(self):
        self.lin1 = nn.Linear(
            self.dim, self.width, bias=False
        ).to(nnGlobals.device)

        # this input is a tensor

    def run(self, matrix):
        print("running lin")
        if (self.setup):
            self.dim = matrix.size(-1)
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        data = self.lin1(matrix)
        print("printing linear", data.shape)
        return data


class nnEmbedings(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        self.token_embedding_table = None
        self.position_embedding_table = None
        self.embs = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makeembs()

    def get_user_data(self):
        self.embs = self.nn_panel.embs.get()
        nnGlobals.emb_dims = self.embs

    def set_user_data(self):
        self.token_embedding_table = nn.Embedding(
            nnGlobals.vocab_size, self.embs).to(nnGlobals.device)
        self.position_embedding_table = nn.Embedding(
            nnGlobals.block_size, self.embs).to(nnGlobals.device)

    def run(self, matrix):
        print("running embs")
        if (self.setup):
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        B, T = matrix.shape

        tok_emb = self.token_embedding_table(matrix)
        pos_emb = self.position_embedding_table(
            torch.arange(T, device=nnGlobals.device)
        )

        # Combine representations
        x = tok_emb + pos_emb
        print(x.shape)

        return x


class nnMultiply(getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)

        self.transposea = None
        self.transposeb = None
        self.a = None
        self.b = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makemult()

    def get_user_data(self):
        self.transposea = self.nn_panel.transposea.get()
        self.transposeb = self.nn_panel.transposeb.get()

    def set_user_data(self):
        pass

    def run(self, matrix):
        print("running embs")
        if (self.setup):
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        if (self.a is not None):
            # run multiplication
            if (self.transposea):
                self.a = self.a.transpose(-2, -1)
            if (self.transposeb):
                matrix = matrix.transpose(-2, -1)

            print(self.a.shape)
            print(matrix.shape)
            if (self.a.size(-1) != matrix.size(-2)):
                print("items not compatible")
                matrix = None
            else:
                matrix = matrix @ self.a

            self.a = None
            return matrix
        else:
            self.a = matrix
            return None


class nnScript(getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)

        self.exec_file = None
        self.prog = None
        self.setup = True
        self.count = 0

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makescript(self.filesave)

    def filesave(self):
        pass

    def fileget(self):
        # set the entry to the file
        pass

    def get_user_data(self):
        self.exec_file = self.nn_panel.filename.get()
        self.prog = self.nn_panel.prog.get()

    def set_user_data(self):
        pass

    def run(self, matrix):
        print("running script")
        if (self.setup):
            self.fileget()
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        # locals are removed anyways
        # local_scope = {}
        exec_scope = {
            'torch': torch,
            'device': nnGlobals.device,
            'x': matrix,
            'y': nnGlobals.y,
            'count': self.count
        }

        # 2. Pass the dictionary into the globals parameter of exec()
        # exec("c = x.sum(1, keepdim=False)", exec_scope)
        exec(self.prog, exec_scope)

        # 3. Extract your new tensor 'c' from the environment dictionary
        c = exec_scope['c']
        print(c.shape)
        self.count += 1
        return c


class nnRelu(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        self.relu = nn.Relu()
        self.setup = False

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makelin()

    def get_user_data(self):
        pass

    def set_user_data(self):
        pass

    def run(self, matrix):
        print("running relu")
        return self.relu(matrix)


class nnDropout(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        self.drop = None
        self.dropval = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makelin()

    def get_user_data(self):
        self.dropval = self.nn_panel.spinvar.get()

    def set_user_data(self):
        self.drop = nn.dropout(self.dropval)

    def run(self, matrix):
        print("running dropout")
        if (self.setup):
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        return self.drop(matrix)


# TODO: fix maybe?
class nnLayerNorm(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        self.lay = None
        self.setup = True
        self.dim = None

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makelin()

    def get_user_data(self):
        pass

    def set_user_data(self):
        self.lay = nn.LayerNorm(self.dim)

    def run(self, matrix):
        print("running layerNorm")
        if (self.setup):
            self.dim = matrix.size(-1)
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        return self.lay(matrix)


class nnSplit(getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)

        self.fraction = None
        self.block = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.makesplit()

    def get_user_data(self):
        self.fraction = self.nn_panel.fraction.get()
        self.block = self.nn_panel.block.get()

    def set_user_data(self):
        pass

    def run(self, matrix):
        print("running split")
        if (self.setup):
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        remainder = matrix.size(-1) % self.fraction
        if (remainder == 0 and self.block <= self.fraction):
            chunks = torch.chunk(
                matrix, chunks=self.fraction, dim=-1
            )
            print(matrix.shape)
            print(chunks[0].shape)
            return chunks[self.block-1]
        else:
            print("invlaid")
            return None


class nnTril(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        # self.tril = None # do not uncomment
        self.dima = None
        self.dimb = None
        self.ones = None
        self.setup = True

        # panel data
        self.nn_panel = my_panel_maker.maketril()

    def get_user_data(self):
        pass

    def set_user_data(self):
        device = nnGlobals.device
        ones = torch.ones(self.dima, self.dimb)
        ones.to(nnGlobals.device)
        self.register_buffer('tril', torch.tril(ones).to(device))

    def run(self, matrix):
        print("running tril")
        if (self.setup):
            self.dima = matrix.size(-2)
            self.dimb = matrix.size(-1)
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        data = matrix.masked_fill(
            self.tril[:self.dima, :self.dimb] == 0, float('-inf')
        )
        print(data.shape)
        return data


# for the dropdown modify filename on creation
# TODO:

class nnCustom(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        self.filename = None
        self.jsonlist = None
        self.followdict = None
        self.itemlist = []
        self.followdict = None
        self.output = None
        self.setup = True

        # panel data
        self.nn_panel = my_panel_maker.maketril()

    def get_user_data(self):
        with open("lib1.json", 'r', encoding="utf-8") as f:
            text = f.read()

        json_items = json.loads(text)
        self.jsonlist = json_items["itemlist"]
        self.followdict = json_items["followdict"]

    def set_user_data(self):
        deserializer = basicdeserial()
        for item in self.jsonlist:
            temp_item = deserializer.deserialize(item)
            self.itemlist.append(temp_item)
            print(temp_item.typename)

    def callnexts(self, prev, index, itemlist):
        curr = itemlist[index]
        if (curr.typename == "Terminate"):
            self.output = prev
            return

        out = curr.run(prev)
        # grab next indeces and call them with out
        for next_ind in self.followdict[str(index)]:
            self.callnexts(out, next_ind, itemlist)

    def run(self, matrix):
        print("running custom")
        if (self.setup):
            self.get_user_data()
            self.set_user_data()
            self.setup = False

        self.callnexts(matrix, 0, self.itemlist)
        print(self.output.shape)

        return self.output


class nnTerminate(nn.Module, getsetpanel):
    def __init__(self, my_panel_maker):
        control_panel = my_panel_maker.control_panel
        getsetpanel.__init__(self, control_panel)
        nn.Module.__init__(self)

        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.nn_panel = my_panel_maker.maketril()

    def get_user_data(self):
        pass

    def set_user_data(self):
        pass

    def run(self, matrix):
        print("running terminate")
        if (self.setup):
            self.setup = False

        return matrix
