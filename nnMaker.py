from control import nnItem
from items import nnStart, nnGlobals, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril
from basicItems import basicLinear,  basicMultiply, basicScript, basicSplit, basicTril, basicDropout
# this is a comment
# TODO: make this its own file/class


class nnMaker:
    def __init__(self, my_panel_maker, controller, ddCanvas):
        self.my_panel_maker = my_panel_maker
        self.controller = controller
        self.ddCanvas = ddCanvas

    def get_nn_item(self, selection):
        pm = self.my_panel_maker
        match selection:
            case "Start": return nnStart(pm)
            case "Batch": return nnBatch(pm)
            case "Multiply": return nnMultiply(pm)
            case "Split": return nnSplit(pm)
            case "Script": return nnScript(pm)
            case "Embeddings": return nnEmbedings(pm)
            case "Linear": return nnLinear(pm)
            case "Tril": return nnTril(pm)
            case _: return None

    def make_nnItem(self, selection):
        ddCanvas = self.ddCanvas

        print("running make")
        ddCanvas.state = selection

        nn_item = self.get_nn_item(selection)

        if selection in {"Embeddings", "Linear", "Tril"}:
            nn_item.to(nnGlobals.device)

        my_nnItem = None
        if (nn_item is not None):
            my_nnItem = nnItem(nn_item, selection)
            ddCanvas.add_canvas_item(my_nnItem)
            self.controller.itemlist.append(my_nnItem)

        return my_nnItem


class basicMaker:
    def __init__(self, device):
        self.device = device

    def get_basic_item(self, selection, *args):
        match selection:
            case "Relu": return basicLinear()
            case "Multiply": return basicMultiply(args)
            case "Split": return basicSplit(args)
            case "Script": return basicScript(args)
            case "Tril": return basicTril(self.device)
            case "LayerNorm": return basicTril(self.device)
            case "Linear": return basicLinear(self.device, args)
            case "Dropout": return basicDropout(self.device, args)
            case _: return None
