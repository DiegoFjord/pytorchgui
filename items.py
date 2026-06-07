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
        print("this is a panel")
        self.control_panel.add(self.start_panel.panel)

    def hide_user_panel(self):
        print("this is a panel")
        self.control_panel.forget(self.start_panel.panel)

    def readfile(self):
        # with open(self.filename, 'r', encoding="utf-8") as f:
        # text = f.read()

        text = "this is some, text 1"
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


# input all data
# batched data
class batchData:
    def __init__(self):
        self.batch_size = None
        self.block_size = None
        self.train_data = None
        self.val_date = None

    def parse_data(self, data):
        n = int(0.9*len(data))  # first 90% will be train, rest val
        self.train_data = data[:n]
        self.val_data = data[n:]

    # used for self supervised learning
    def get_batch(self, train_data, val_data, split):  # returns a (batch x block) tensor
        # generate a small batch of data of inputs x and targets y
        data = train_data if split == 'train' else val_data
        ix = torch.randint(len(data) - self.block_size, (self.batch_size,))
        x = torch.stack([data[i:i+self.block_size] for i in ix])
        y = torch.stack([data[i+1:i+self.block_size+1] for i in ix])
        x, y = x.to(device), y.to(device)
        return x, y

    def get_user_data(self):
        # temp values (get all of the none values)
        self.n_emb = 1

    def run(self, matrix):
        self.get_user_data()
        self.parse_data(matrix)
        return None


# using this to test the pytorch -1 tensors
class nnTest:
    def __init__(self, my_panel_maker):
        self.lin1 = nn.LazyLinear(10)
        self.control_panel = my_panel_maker.control_panel
        self.test_panel = self.my_panel_maker.maketest()

    def get_user_panel(self):
        print("this is a panel")
        self.control_panel.add(self.test_panel.panel)

    def hide_user_panel(self):
        print("this is a panel")
        self.control_panel.forget(self.test_panel.panel)

    def run(self, matrix):
        # self.get_user_data()
        # self.parse_data(matrix)
        data = self.lin1(matrix)
        print("the test data", data)
        return data


class nnLinear:
    def __init__(self, my_panel_maker):
        self.lin1 = nn.LazyLinear(10)
        self.control_panel = my_panel_maker.control_panel
        self.lin_panel = my_panel_maker.makelin()

    def get_user_panel(self):
        print("get panel")
        self.control_panel.add(self.lin_panel.panel)

    def hide_user_panel(self):
        print("unset panel")
        self.control_panel.forget(self.lin_panel.panel)

    # this input is a tensor

    def run(self, matrix):
        # self.get_user_data()
        # self.parse_data(matrix)
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
