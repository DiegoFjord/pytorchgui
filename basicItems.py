import torch.nn as nn
import torch


class basicLinear(nn.Module):
    def __init__(self, device, width):
        nn.Module.__init__(self)

        self.device = device

        self.lin1 = None

        self.dim = None
        self.width = width

        self.setup = True

    def set_user_data(self):
        self.lin1 = nn.Linear(
            self.dim, self.width, bias=False
        ).to(self.device)

    def run(self, matrix):
        print("running lin")
        if (self.setup):
            self.dim = matrix.size(-1)
            self.set_user_data()
            self.setup = False

        data = self.lin1(matrix)
        return data


class basicMultiply():
    def __init__(self, transposea, transposeb, a, b):
        self.transposea = transposea
        self.transposeb = transposeb
        self.a = a
        self.b = b

        self.setup = True

    def run(self, matrix):
        print("running embs")
        if (self.setup):
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


class basicScript():
    def __init__(self, prog):
        self.prog = prog
        self.count = 0

    def run(self, matrix):
        print("running script")

        exec_scope = {
            'torch': torch,
            'x': matrix,
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


class basicSplit():
    def __init__(self, fraction, block):
        self.fraction = fraction
        self.block = block

        self.setup = True

    def run(self, matrix):
        print("running split")
        if (self.setup):

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


class basicRelu(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.relu = nn.Relu()

    def run(self, matrix):
        print("running relu")
        return self.relu(matrix)


class basicDropout(nn.Module):
    def __init__(self, device, dropval):
        nn.Module.__init__(self)
        self.device = device

        self.drop = None
        self.dropval = dropval

        self.setup = True

    def set_user_data(self):
        self.drop = nn.dropout(self.dropval).to(self.device)

    def run(self, matrix):
        print("running relu")
        if (self.setup):
            self.set_user_data()
            self.setup = False

        return self.drop(matrix)


class basicLayerNorm(nn.Module):
    def __init__(self, device):
        nn.Module.__init__(self)
        self.device = device

        self.lay = None

        self.dim = None

        self.setup = True

    def set_user_data(self):
        self.lay = nn.LayerNorm(self.dim).to(self.device)

    def run(self, matrix):
        print("running relu")
        if (self.setup):
            self.dim = matrix.size(-1)

            self.set_user_data()
            self.setup = False

        return self.lay(matrix)


class basicTril(nn.Module):
    def __init__(self, device):
        nn.Module.__init__(self)
        self.device = device

        # self.tril = None # do not uncomment
        self.dima = None
        self.dimb = None
        self.ones = None

        self.setup = True

    def set_user_data(self):
        ones = torch.ones(self.dima, self.dimb)
        self.register_buffer(
            'tril', torch.tril(ones).to(self.device)
        ).to(self.device)

    def run(self, matrix):
        print("running tril")
        if (self.setup):
            self.dima = matrix.size(-2)
            self.dimb = matrix.size(-1)

            self.set_user_data()
            self.setup = False

        data = matrix.masked_fill(
            self.tril[:self.dima, :self.dimb] == 0, float('-inf')
        )
        print(data)
        return data
