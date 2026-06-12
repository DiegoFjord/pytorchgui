import re
import torch.nn as nn
import torch
import torch_directml
# my imports

# NOTE: maybe make a gobals class

# global vars


class nnGlobals:
    vocab_size = None
    block_size = None
    batch_size = None
    emb_dims = None
    device = torch_directml.device()


class nnStart:
    def __init__(self, filename, my_panel_maker):
        # file
        self.filename = None
        self.execution = None
        self.setup = True

        # rendering
        self.control_panel = my_panel_maker.control_panel
        self.start_panel = my_panel_maker.makestart()

    def get_user_panel(self):
        self.control_panel.add(self.start_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.start_panel.panel)

    def set_user_data(self):
        self.filename = self.start_panel.entry.get()
        self.execution = self.start_panel.execute.get()

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
            return torch.rand(16, 8, 4)
        if (self.execution == 2):
            return self.readfile()
    # this input is a tensor

    def run(self, matrix):
        print("running start")
        if (self.setup):
            self.set_user_data()
            self.setup = False

        data = self.runExecute()
        # fetch control_panel values on run
        # run other important stuff
        print(data.shape)
        return data


# input starting data
# output training data and holds desired output
# forwards to the nn to train and find loss
class nnBatch:
    def __init__(self, my_panel_maker):
        self.train_data = None
        self.val_date = None
        self.split = None
        self.setup = True

        self.control_panel = my_panel_maker.control_panel
        self.batch_panel = my_panel_maker.makebatch()

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
        # nnGlobals.y = y
        return x

    def get_user_panel(self):
        self.control_panel.add(self.batch_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.batch_panel.panel)

    def set_user_data(self):
        # TODO: handle non numeric input
        nnGlobals.batch_size = self.batch_panel.batch.get()
        nnGlobals.block_size = self.batch_panel.block.get()
        split = self.batch_panel.split.get()
        if (split == 1):
            self.split = "train"
        else:
            self.split = "val"

    def run(self, matrix):
        print("running batch")
        if (self.setup):
            self.set_user_data()
            self.parse_data(matrix)
            self.setup = False

        x = self.get_batch(
            matrix, matrix, self.split,
            nnGlobals.batch_size, nnGlobals.block_size
        )

        print(x.shape)
        return x


class nnLinear(nn.Module):
    def __init__(self, my_panel_maker):
        super().__init__()
        self.lin1 = None
        self.dim = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.lin_panel = my_panel_maker.makelin()

    def get_user_panel(self):
        self.control_panel.add(self.lin_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.lin_panel.panel)

    def set_user_data(self):
        # TODO: handle non numeric input
        linval = self.lin_panel.spinvar.get()
        self.lin1 = nn.Linear(
            self.dim, linval, bias=False
        ).to(nnGlobals.device)

        # this input is a tensor

    def run(self, matrix):
        print("running lin")
        if (self.setup):
            self.dim = matrix.size(-1)
            self.set_user_data()
            self.setup = False

        data = self.lin1(matrix)
        print("printing linear", data.shape)
        return data


class nnEmbedings(nn.Module):
    def __init__(self, my_panel_maker):
        super().__init__()

        self.token_embedding_table = None
        self.position_embedding_table = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.embs_panel = my_panel_maker.makeembs()

    def get_user_panel(self):
        self.control_panel.add(self.embs_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.embs_panel.panel)

    def set_user_data(self):
        embval = self.embs_panel.embs.get()
        nnGlobals.emb_dims = embval

        self.token_embedding_table = nn.Embedding(
            nnGlobals.vocab_size, embval).to(nnGlobals.device)
        self.position_embedding_table = nn.Embedding(
            nnGlobals.block_size, embval).to(nnGlobals.device)

    def run(self, matrix):
        print("running embs")
        if (self.setup):
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


class nnMultiply:
    def __init__(self, my_panel_maker):
        super().__init__()
        self.transposea = None
        self.transposeb = None
        self.a = None
        self.b = None
        self.setup = True

        # panel data
        self.control_panel = my_panel_maker.control_panel
        self.mult_panel = my_panel_maker.makemult()

    def get_user_panel(self):
        self.control_panel.add(self.mult_panel.panel)

    def hide_user_panel(self):
        self.control_panel.forget(self.mult_panel.panel)

    def set_user_data(self):
        self.transposea = self.mult_panel.transposea.get()
        self.transposeb = self.mult_panel.transposeb.get()

    def run(self, matrix):
        print("running embs")
        if (self.setup):
            self.set_user_data()
            self.setup = False

        if (self.a is not None):
            # run multiplication
            if (self.transposea == 1):
                self.a = self.a.transpose(-2, -1)
            if (self.transposeb == 1):
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
