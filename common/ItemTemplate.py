

class ItemTemplate():

    EMPTY_TAGS_STRING = ""

    def __init__(self, name, path, level, type_id, shape, initial_uses, type_tags):
        self.name = name
        self.path = path
        self.level = level
        self.type_id = type_id
        self.shape = shape
        self.initial_uses = initial_uses
        self.type_tags = type_tags

        self.type_tags_set = None

    def get_type_set_without_condition(self):
        return self.type_tags_set

    def get_type_set(self):
        if self.type_tags_set is None:
            self.type_tags_set = set(self.type_tags.split(","))
            self. get_type_set = self.get_type_set_without_condition
            return self.type_tags_set

    def has_tag(self, tag):
        return tag in self.get_type_set()

    def __str__(self):
        return "ItemTemplate - (Name, %s) - (Id, %s) - (Tags, %s)" % (str(self.name), str(self.type_id), self.type_tags)

    @staticmethod
    def from_dict(dictionary):
        return ItemTemplate(dictionary['name'], dictionary['path'], dictionary['level'], dictionary['type_id'], dictionary['shape'], dictionary['initial_uses'], dictionary['type_tags'])


