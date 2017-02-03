# -*- coding:utf-8 -*-


class SupportsDrop():

    def __init__(self):
        pass

    def finish_drop(self, item):
        raise NotImplementedError


class SupportsDrag():

    def __init__(self):
        pass

    def notify_accepted(self, item):
        raise NotImplementedError


class GuiDragDropService():
    """ This class is the gloabl know instance which holds the info abput things being dragged or dropped and therefore
        can be used as syncronisation point between several systems that do drag and drop """

    def __init__(self):
        self.currently_dragged_item = None
        self.droppables = []

    def has_dragged_item(self):
        return self.currently_dragged_item is not None

    def put_dragged_item(self, element, dragged_item):
        print "Requesting drag from", element, dragged_item
        self.currently_dragged_item = (element, dragged_item)

    def get_dragged_item(self):
        return self.currently_dragged_item[1]

    def cancel_drag_drop(self):
        accepted = False
        who = None
        for droppable in self.droppables:
            accepted = accepted or droppable.finish_drop(self.currently_dragged_item)
            if accepted:
                who = droppable
                break

        if accepted and who != self.currently_dragged_item[0]:
            self.currently_dragged_item[0].notify_accepted(self.currently_dragged_item[1])

        self.currently_dragged_item = None

    def register_me_on_drop(self, droppable):
        self.droppables.append(droppable)


class ItemDrag():

    def __init__(self, item, mx, my):
        self.item = item
        self.mx = mx
        self.my = my

    def get_itemuid(self):
        return self.item.get_uid()

    def get_item(self):
        return self.item
