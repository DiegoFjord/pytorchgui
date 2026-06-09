import re
import torch.nn as nn
import torch
import torch_directml
# my imports
device = torch_directml.device()

# NOTE: maybe make a gobals class

# global vars
vocab_size = 0


# add embeddings to data
class nnStart:
    def __init__(self, filename, my_panel_maker):
        # file
        self.name = filename

        # data
        self.block_size = 8  # context length
        self.batch_size = 8  # number of blocks

        # user input data

        # rendering
        self.control_panel = my_panel_maker.control_panel
        self.start_panel = my_panel_maker.makestart()

    def get_user_panel(self):
        self.control_panel.add(self.start_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.start_panel.panel)

    def readfile(self):
        # with open(self.filename, 'r', encoding="utf-8") as f:
        # text = f.read()

        text = """this is some, text 1 that is longet than the previous text
           a b c d e f g h i j k l m n o p q r s t u v w x y z
        """
        # NOTE: tokens
        tokens = re.findall(r"\w+|\s|[^\w\s]", text.lower())

        tokenset = set(tokens)
        tokensetlist = list(tokenset)

        global vocab_size
        vocab_size = len(tokensetlist)

        # TODO: tokenize strings not chars
        stoi = {ch: i for i, ch in enumerate(tokensetlist)}
        itos = {i: ch for i, ch in enumerate(tokensetlist)}

        def encode(s): return [stoi[c] for c in s]
        def decode(b): return ''.join([itos[i] for i in b])

        data = torch.tensor(encode(tokens), dtype=torch.float)
        print(data)
        return data

    # this input is a tensor
    def run(self, matrix):
        data = self.readfile()
        # fetch control_panel values on run
        # run other important stuff
        print("the start data", data)
        return data


# input starting data
# output training data and holds desired output
# forwards to the nn to train and find loss
class nnBatch:
    def __init__(self, my_panel_maker):
        self.batch_size = None
        self.block_size = None
        self.train_data = None
        self.val_date = None
        self.split = None

        self.y = None

        self.control_panel = my_panel_maker.control_panel
        self.batch_panel = my_panel_maker.makebatch()

    def parse_data(self, data):
        n = int(0.9*len(data))  # first 90% will be train, rest val
        self.train_data = data[:n]
        self.val_data = data[n:]

    # used for self supervised learning
    # returns a (batch x block) tensor
    def get_batch(self, train_data, val_data, split):
        # generate a small batch of data of inputs x and targets y
        data = train_data if split == 'train' else val_data
        ix = torch.randint(len(data) - self.block_size, (self.batch_size,))
        x = torch.stack([data[i:i+self.block_size] for i in ix])
        y = torch.stack([data[i+1:i+self.block_size+1] for i in ix])
        x, y = x.to(device), y.to(device)
        self.y = y
        return x

    def get_user_panel(self):
        self.control_panel.add(self.batch_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.batch_panel.panel)

    def set_user_data(self):
        # TODO: handle non numeric input
        self.batch_size = self.batch_panel.batch.get()
        self.block_size = self.batch_panel.block.get()
        print("batch and block", self.batch_size, self.block_size)
        self.split = self.batch_panel.split.get()

    def run(self, matrix):
        self.set_user_data()
        self.parse_data(matrix)
        x = self.get_batch(self.train_data, self.val_data, self.split)
        return x


class nnLinear:
    def __init__(self, my_panel_maker):
        self.lin1 = None

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.lin_panel = my_panel_maker.makelin()

    def get_user_panel(self):
        self.control_panel.add(self.lin_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.lin_panel.panel)

    def set_user_data(self):
        # TODO: handle non numeric input
        linval = self.lin_panel.spinvar
        self.lin1 = nn.LazyLinear(linval.get())

        # this input is a tensor

    def run(self, matrix):
        self.set_user_data()
        data = self.lin1(matrix)
        print("the lin data", data)
        return data


class gate:
    def __init__(self, name):
        self.name = name


class notepad:
    def __init__(self, name):
        self.name = name


class nnRelu:
    def __init__(self):
        self.relu = nn.Relu()

    # this input is a tensor
    def run(self, InputNode):
        return self.relu(InputNode)


class nnDropout:
    def __init__(self, dropout):
        self.drop = nn.dropout(dropout)

    # this input is a tensor
    def run(self, InputNode):
        return self.drop(InputNode)


class nnLayerNorm:
    def __init__(self):
        self.ln = None

    # this input is a tensor
    def run(self, InputNode):
        if (not self.ln):
            embs = InputNode.shape[0]
            self.ln = nn.LayerNorm(embs)

        return self.lin(InputNode)
