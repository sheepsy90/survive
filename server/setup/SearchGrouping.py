# -*- coding:utf-8 -*-


class DropElement():

    def __init__(self, drop_chance, path, level):
        self.drop_chance = drop_chance
        self.path = path
        self.level = level

    def __str__(self):
        return "Drop Element (%i, %s, %i)" % (self.drop_chance, self.path, self.level)


class SearchGrouping():

    def __init__(self, identifier, name, size, num_items):
        # General Parameters
        self.identifier = identifier
        self.name = name
        self.size = size
        self.num_items = num_items

        # The List of drops
        self.drop_elements = []

    def get_number_items_to_spawn(self):
        return self.num_items

    def get_size(self):
        return self.size

    def get_drop_element_list(self):
        return self.drop_elements

    def add_drop_path(self, drop_element):
        self.drop_elements.append(drop_element)

    def __str__(self):
        return "Id: %i - Name: %s - Size: %s\n\t" % (self.identifier, self.name, str(self.size)) + \
                "\n\t".join([str(e) for e in self.drop_elements])


class SearchGroupingManager():

    def __init__(self):
        # The general dict of search groupings
        self.search_grouping_dict = {}

        sg = SearchGrouping(1, "first_aid_kit", (6, 5), (1, 4))
        sg.add_drop_path(DropElement(10, "item/medical/basics", 1))
        self.search_grouping_dict[sg.name] = sg

        sg1 = SearchGrouping(2, "steel_cupboard", (6, 5), (2, 5))
        sg1.add_drop_path(DropElement(2, "item/medical/basics", 3))
        sg1.add_drop_path(DropElement(5, "item/medical/basics", 2))
        sg1.add_drop_path(DropElement(10, "item/medical/basics", 1))
        self.search_grouping_dict[sg1.name] = sg1

        sg3 = SearchGrouping(2, "lunch_package", (8, 6), (3, 5))
        sg3.add_drop_path(DropElement(10, "item/drink/bottles", 1))
        self.search_grouping_dict[sg3.name] = sg3

        sg2 = SearchGrouping(3, "server_rack", (6, 5), (1, 4))
        self.search_grouping_dict[sg2.name] = sg2

        print sg

    def get_search_grouping_by_name(self, name):
        return self.search_grouping_dict.get(name, None)