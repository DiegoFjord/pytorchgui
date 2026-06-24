from control import nnItem
from items import nnStart, nnGlobals, nnLinear, nnBatch, nnEmbedings, nnMultiply, nnScript, nnSplit, nnTril, nnCustom
from basicItems import basicLinear, basicMultiply, basicScript, basicSplit, basicTril, basicDropout, basicTerminate
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
            case "Custom": return nnCustom(pm)
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
    def get_basic_item(self, selection):
        match selection:
            # set selection in the constructor
            case "Relu": return basicLinear(selection)
            case "Multiply": return basicMultiply(selection)
            case "Split": return basicSplit(selection)
            case "Script": return basicScript(selection)
            case "Tril": return basicTril(selection)
            case "LayerNorm": return basicTril(selection)
            case "Linear": return basicLinear(selection)
            case "Dropout": return basicDropout(selection)
            case "Terminate": return basicTerminate(selection)
            case _: return None
