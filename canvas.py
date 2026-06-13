# this is a comment
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

# TODO: label id items ass nn_xxx_id


class DragDropCanvas:
    def __init__(self, canvas, controller):
        # breakpoint()
        self.controller = controller

        # Create canvas
        self.canvas = canvas

        # Create start
        start_id = self.canvas.create_rectangle(
            50, 50, 150, 150, fill="yellow"
        )
        self.controller.itemset[start_id] = controller.treeStart
        self.controller.itemset[start_id].curr.get_user_panel()

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Variables to track mouse position and selected item
        self.state = None  # set to mouse linear...
        self.base_id = None  # the first item selcted(used for line)
        self.selected_id = None  # current item selected for drawing
        self.last = start_id  # last/current item selected
        self.start_x = 0
        self.start_y = 0

    def add_canvas_item(self, bind):
        # Create a draggable rectangle
        color = None
        if (bind.nntype == "Batch"):
            color = "darkblue"
        elif (bind.nntype == "Embeddings"):
            color = "green"
        elif (bind.nntype == "Linear"):
            color = "light blue"
        elif (bind.nntype == "Script"):
            color = "light pink"
        else:
            color = "red"

        item_id = self.canvas.create_rectangle(
            50, 50, 150, 150, fill=color
        )
        self.controller.itemset[item_id] = bind
        print(f"made {item_id}")

    def get_line_coors(self, x0, y0, x1, y1):
        midx = x0 + (x1 - x0)/2
        parcurve = [
            x0, y0,
            midx, y0,
            midx, y1,
            x1, y1
        ]
        return parcurve

    def set_control_panel(self, tempdict, clicked_id):
        tempdict[self.last].curr.hide_user_panel()
        tempdict[clicked_id].curr.get_user_panel()
        self.last = clicked_id

    def on_press(self, event):
        """Detects if an item was pressed."""
        # Find the item closest to the click coordinates
        clicked_ids = self.canvas.find_withtag("current")

        tempdict = self.controller.itemset

        if clicked_ids:
            clicked_id = clicked_ids[0]
            self.start_x = event.x
            self.start_y = event.y

            if (clicked_id in self.controller.itemset):
                self.set_control_panel(tempdict, clicked_id)
                self.base_id = clicked_id
                if (self.state == "Line"):
                    initial_points = [
                        event.x, event.y,
                        event.x, event.y,
                        event.x, event.y,
                        event.x, event.y
                    ]

                    item_id = self.canvas.create_line(
                        initial_points, smooth=True, fill="blue", width=3.0
                    )

                    self.selected_id = item_id

                else:
                    self.selected_id = clicked_ids[0]

    def on_drag(self, event):
        """Drags the selected item."""
        if self.selected_id:
            # Calculate how far the mouse moved
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            tempdict = self.controller.itemset

            # Move the item by the offset distance
            if (self.state == "Mouse"):
                self.canvas.move(self.selected_id, dx, dy)
                # update the line attached to the item
                for lineend in tempdict[self.selected_id].line_prevs:
                    curr_coords = self.canvas.coords(lineend)
                    self.canvas.coords(
                        lineend,
                        *self.get_line_coors(
                            curr_coords[0],
                            curr_coords[1],
                            curr_coords[6] + dx,
                            curr_coords[7] + dy)
                    )
                for linestart in tempdict[self.selected_id].line_nexts:
                    curr_coords = self.canvas.coords(linestart)
                    self.canvas.coords(
                        linestart,
                        *self.get_line_coors(
                            curr_coords[0] + dx,
                            curr_coords[1] + dy,
                            curr_coords[6],
                            curr_coords[7]
                        )
                    )

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

        if (nntype == "Multiply"):
            if (len(tempdict[target_id].prevs) > 1):
                return False
        elif (len(tempdict[target_id].prevs) > 0):
            return False

        return True

    def attach_line(self, tempdict, base_id,  target_id, selected_id,):
        # line segment attaching to next and previous
        tempdict[self.base_id].line_nexts.append(
            self.selected_id
        )
        tempdict[target_id].line_prevs.append(
            self.selected_id)

        # logical next and previous
        tempdict[self.base_id].nexts.append(
            tempdict[target_id]
        )
        tempdict[target_id].prevs.append(
            tempdict[self.base_id]
        )

    def on_release(self, event):
        """Detects when the mouse button is released."""
        tempdict = self.controller.itemset
        target_id = -1

        clicked_ids = self.canvas.find_overlapping(
            event.x, event.y, event.x, event.y
        )

        if clicked_ids and self.base_id:
            # id of item found on release
            for item_id in clicked_ids:
                if (item_id in tempdict):
                    target_id = item_id

            # aka is a line
            if (self.selected_id not in tempdict):
                # if line has a valid line endpoint
                if (self.line_target_conditions(tempdict, target_id)):
                    self.attach_line(
                        tempdict, self.base_id, target_id, self.selected_id
                    )
                else:
                    self.canvas.delete(self.selected_id)

        # reset the selection
        if self.selected_id:
            self.selected_id = None
        if self.base_id:
            self.base_id = None
