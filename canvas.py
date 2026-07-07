# this is a comment
from designer import designer
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


# TODO: label id items ass nn_xxx_id


class DragDropCanvas:
    def __init__(self, canvas, controller):
        # breakpoint()
        self.controller = controller
        self.my_designer = designer(canvas)

        # Create canvas
        self.canvas = canvas

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Delete>", self.on_delete)
        # Variables to track mouse position and selected item
        self.state = None  # set to mouse linear...
        self.base_id = None  # the first item selcted(used for line)
        self.selected_id = None  # current item selected for drawing
        self.last = None  # last/current item selected
        self.start_x = 0
        self.start_y = 0
        self.item_dict = {}

    def add_canvas_item(self, bind):
        # Create a draggable rectangle
        item_id = self.my_designer.getbystring(bind.nntype)
        self.controller.itemset[item_id] = bind
        self.set_control_panel(self.controller.itemset, item_id)

    def get_line_coors(self, x0, y0, x1, y1):
        midx = x0 + (x1 - x0)/2
        parcurve = [
            x0, y0,
            midx, y0,
            midx, y1,
            x1, y1
        ]
        return parcurve

    def on_delete(self, e):
        print("deleting")

        tempItem = self.controller.itemset[self.last]
        tempItem.curr.hide_user_panel()
        prevlines = tempItem.line_nexts
        nextlines = tempItem.line_prevs

        for line in prevlines:
            self.canvas.delete(line)
        for line in nextlines:
            self.canvas.delete(line)

        if (self.last is not None):
            self.canvas.delete(self.last)
            self.my_designer.delete(self.last)

        self.controller.remove_item(tempItem, self.last)

        self.last = None
        self.selected_id = None
        self.base_id = None

    def set_control_panel(self, tempdict, clicked_id):
        if (self.last is not None):
            tempdict[self.last].curr.hide_user_panel()
        tempdict[clicked_id].curr.get_user_panel()
        self.last = clicked_id

    def on_press(self, e):
        tempdict = self.controller.itemset

        clicked_ids = self.canvas.find_overlapping(
            e.x, e.y, e.x, e.y
        )

        for clicked_id in reversed(clicked_ids):
            if (clicked_id in tempdict):
                self.start_x = e.x
                self.start_y = e.y

                self.set_control_panel(tempdict, clicked_id)
                self.base_id = clicked_id
                if (self.state == "Line"):
                    initial_points = [e.x, e.y, e.x, e.y, e.x, e.y, e.x, e.y]

                    item_id = self.canvas.create_line(
                        initial_points, smooth=True, fill="blue", width=3.0)

                    self.selected_id = item_id

                else:
                    self.selected_id = clicked_id

                break

    def move_end(self, line_id, a, b, c, d):
        curr_coords = self.canvas.coords(line_id)
        self.canvas.coords(
            line_id,
            *self.get_line_coors(
                curr_coords[0] + a,
                curr_coords[1] + b,
                curr_coords[6] + c,
                curr_coords[7] + d)
        )

    def on_drag(self, event):
        """Drags the selected item."""
        if self.selected_id:
            # Calculate how far the mouse moved
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            tempdict = self.controller.itemset

            # Move the item by the offset distance
            if (self.state != "Line"):
                self.canvas.move(self.selected_id, dx, dy)
                self.my_designer.move(self.selected_id, dx, dy)
                # update the line attached to the item
                for lineend in tempdict[self.selected_id].line_prevs:
                    self.move_end(lineend, 0, 0, dx, dy)
                for linestart in tempdict[self.selected_id].line_nexts:
                    self.move_end(linestart, dx, dy, 0, 0)
                # Update the starting position for the next movement frame
                self.start_x = event.x
                self.start_y = event.y
            elif (self.state == "Line"):
                self.canvas.coords(
                    self.selected_id,
                    *self.get_line_coors(
                        self.start_x, self.start_y, event.x, event.y
                    )
                )

    def line_target_conditions(self, tempdict, target_id):

        if (target_id < 0):
            return False

        if (self.base_id == target_id):
            return False

        nntype = tempdict[target_id].nntype

        if (nntype == "Start"):
            return False

        if (nntype == "Script"):
            pass
        elif (nntype == "Multiply"):
            if (len(tempdict[target_id].prevs) > 1):
                return False
        elif (len(tempdict[target_id].prevs) > 0):
            return False

        return True

    def get_line(self):
        initial_points = [100, 50, 50, 50, 50, 50, 0, 50]
        return self.canvas.create_line(initial_points, smooth=True, fill="blue", width=3.0)

    def attach_line(self, base_id,  target_id, selected_id,):
        # line segment attaching to next and previous

        tempdict = self.controller.itemset
        tempdict[base_id].line_nexts.append(selected_id)
        tempdict[target_id].line_prevs.append(selected_id)

        # logical next and previous
        tempdict[base_id].nexts.append(tempdict[target_id])
        tempdict[target_id].prevs.append(tempdict[base_id])

    def on_release(self, event):
        """Detects when the mouse button is released."""
        tempdict = self.controller.itemset
        target_id = -1

        clicked_ids = self.canvas.find_overlapping(
            event.x, event.y, event.x, event.y
        )
        print(clicked_ids)

        for item_id in clicked_ids:
            if (item_id in tempdict):
                target_id = item_id

        if (self.state == "Line" and self.base_id):
            if (self.line_target_conditions(tempdict, target_id)):
                self.attach_line(
                    self.base_id, target_id, self.selected_id
                )
            else:
                self.canvas.delete(self.selected_id)

        # reset the selection
        # TODO: maybe set last on release
        if self.selected_id:
            self.selected_id = None
        if self.base_id:
            self.base_id = None
