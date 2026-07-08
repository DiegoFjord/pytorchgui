import torch.nn as nn
import torch
from torch.nn import functional as F
from items import nnGlobals


class basicStart(nn.Module):
    def __init__(self, typename):
        self. typename = typename

    def run(self, matrix):
        return matrix


class basicLinear(nn.Module):
    def __init__(self, typename):
        nn.Module.__init__(self)

        self.device = nnGlobals.device

        self.lin1 = None

        self.dim = None
        self.width = None

        self. typename = typename
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
    def __init__(self, typename):
        self.transposea = None
        self.transposeb = None
        self.a = None
        self.b = None
        self.flip = False

        self. typename = typename
        self.setup = True

    def run(self, matrix):
        print("running mult")
        if (self.setup):
            self.setup = False

        if (self.a is not None):
            # run multiplication
            if (self.transposea):
                matrix = matrix.transpose(-2, -1)
            if (self.transposeb):
                self.a = self.a.transpose(-2, -1)

            print(matrix.shape)
            print(self.a.shape)
            if self.flip:
                if (self.a.size(-1) != matrix.size(-2)):
                    print("items not compatible")
                    matrix = None
                else:
                    matrix = self.a @ matrix
            else:
                if (matrix.size(-1) != self.a.size(-2)):
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
    def __init__(self, typename):
        self.prog = None
        self.count = 1
        self.inputs = []

        self. typename = typename

    def run(self, matrix):
        print("running script")
        self.inputs.append(matrix)

        exec_scope = {
            'torch': torch,
            'x': matrix,
            'y': nnGlobals.y,
            'F': F,
            'inputs': self.inputs,
            'count': self.count
        }

        # 2. Pass the dictionary into the globals parameter of exec()
        # exec("c = x.sum(1, keepdim=False)", exec_scope)
        print("RUNNING PROGRAM ################")
        print(self.prog)
        exec(self.prog, exec_scope)
        print("################################")

        # 3. Extract your new tensor 'c' from the environment dictionary
        out = exec_scope['x']
        print(out.shape)
        self.count += 1
        return out


class basicSplit():
    def __init__(self, typename):
        self.fraction = None
        self.block = None

        self. typename = typename
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
    def __init__(self, typename):
        nn.Module.__init__(self)
        self.relu = nn.Relu()

        self. typename = typename

    def run(self, matrix):
        print("running relu")
        return self.relu(matrix)


class basicDropout(nn.Module):
    def __init__(self, typename):
        nn.Module.__init__(self)
        self.device = nnGlobals.device

        self.drop = None
        self.dropval = None

        self. typename = typename
        self.setup = True

    def set_user_data(self):
        print(self.dropval)
        self.drop = nn.Dropout(self.dropval).to(self.device)

    def run(self, matrix):
        print("running dropout")
        if (self.setup):
            self.set_user_data()
            self.setup = False

        return self.drop(matrix)


class basicLayerNorm(nn.Module):
    def __init__(self, typename):
        nn.Module.__init__(self)
        self.device = nnGlobals.device

        self.lay = None

        self.dim = None

        self. typename = typename
        self.setup = True

    def set_user_data(self):
        self.lay = nn.LayerNorm(self.dim).to(self.device)

    def run(self, matrix):
        print("running layernorm")
        if (self.setup):
            self.dim = matrix.size(-1)

            self.set_user_data()
            self.setup = False

        return self.lay(matrix)


class basicTril(nn.Module):
    def __init__(self, typename):
        nn.Module.__init__(self)
        self.device = nnGlobals.device

        # self.tril = None # do not uncomment
        self.dima = None
        self.dimb = None
        self.ones = None

        self. typename = typename
        self.setup = True

    def set_user_data(self):
        device = nnGlobals.device
        ones = torch.ones(self.dima, self.dimb)
        ones.to(device)
        self.register_buffer('tril', torch.tril(ones).to(device))

    def run(self, matrix):
        print("running tril")
        if (self.setup):
            self.dima = matrix.size(-2)
            self.dimb = matrix.size(-1)
            self.set_user_data()
            self.setup = False

        print(matrix.shape)
        data = matrix.masked_fill(
            self.tril[:self.dima, :self.dimb] == 0, float('-inf')
        )

        return data


class basicTerminate:
    def __init__(self, typename):
        self.typename = "Terminate"
