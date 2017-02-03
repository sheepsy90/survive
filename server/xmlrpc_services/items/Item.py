
class Item(object):

    def __init__(self, item_template, unique_id, uses):
        # TODO need a strategy for creating items with a unique id globally but locally on each area
        # The id which is unique for every item
        self.name = item_template.name
        self.unique_id = unique_id

        # The type id and the shape defining which representation that object gets on a client
        self.item_template = item_template

        # The number of uses left on this item
        # 0 means its indefinitely usable
        # n means it is exactly n times usable
        self.uses = uses

        self.marked_deleting = False

    def mark_deleting(self):
        self.marked_deleting = True

    def is_marked_for_deletion(self):
        return self.marked_deleting

    def get_name(self):
        return self.name

    def get_height(self):
        return self.item_template.shape[1]

    def get_shape(self):
        return self.item_template.shape

    def get_id(self):
        return self.unique_id

    def get_num_usages(self):
        return self.uses

    def get_type_id(self):
        return self.item_template.type_id

    def get_item_template(self):
        return self.item_template

    def decrease_usage_true_on_zero(self):
        self.uses -= 1
        if self.uses == 0:
            return True
        else:
            return False

    def __str__(self):
        return "Item with id %s and num usages left %s" % (str(self.unique_id), str(self.uses))

    def __repr__(self):
        return self.__str__()