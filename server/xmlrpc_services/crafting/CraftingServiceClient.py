import xmlrpclib
from common.ItemTemplate import ItemTemplate
from server.configuration.configuration import Configuration
from server.xmlrpc_services.crafting.CraftingPersistence import CraftingPersistence


class CraftingResult():

    def __init__(self, crafting_representation, result, crafting_dummy, valid_crafting):
        self.crafting_representation = crafting_representation
        self.result = result
        self.crafting_dummy = crafting_dummy
        self.valid_crafting = valid_crafting

    def is_crafting_dummy(self):
        return self.crafting_dummy

    def get_result(self):
        return self.result

    def is_valid_crafting(self):
        return self.valid_crafting

    def __str__(self):
        return "Crafting Recipe for %s - Valid: %s, IsDummy: %s, Results: %s" % \
               (self.crafting_representation, str(self.valid_crafting), str(self.crafting_dummy), str(self.result))


class CraftingServiceClient():

    INVALID_CRAFTING_RESULT = CraftingResult(None, None, None, False)

    def __init__(self):
        # TODO - Add Cache to this ServiceClient
        config = Configuration()
        host, port = config.get_configuration()["CraftingXMLRPC"]
        self.item_service = xmlrpclib.ServerProxy('http://%s:%s' % (str(host), str(port)), allow_none=True)

        self.item_template_cache = {}

    def process_crafting_request(self, crafting_representation):
        """ Process a specific Crafting Recipe """
        if crafting_representation == "":
            return CraftingServiceClient.INVALID_CRAFTING_RESULT

        result = self.item_service.process_crafting_request(crafting_representation)

        print "Crafting Result from Service"

        if result is None:
            return CraftingServiceClient.INVALID_CRAFTING_RESULT

        parsed_result = []
        for element in result:
            template_dict, amount = element
            item_template = ItemTemplate.from_dict(template_dict)
            parsed_result.append([item_template, amount])

        is_dummy = len(parsed_result) == 1 and parsed_result[0][0].name == CraftingPersistence.DUMMY_TYPE_NAME

        return CraftingResult(crafting_representation, parsed_result, is_dummy, result is not None)

    def get_item_template(self, type_id):
        if type_id in self.item_template_cache:
            return self.item_template_cache[type_id]
        else:
            print "Tried to get item template for", type_id
            value = self.item_service.get_item_template(type_id)
            if value is not None:
                item_template = ItemTemplate.from_dict(value)
                self.item_template_cache[type_id] = item_template
                print "Added to cache", item_template
                return item_template
            else:
                return None

    def get_item_types_by_drop_path_and_level(self, drop_path, drop_level):
        result = self.item_service.get_item_types_by_drop_path_and_level(drop_path, drop_level)
        return [ItemTemplate.from_dict(e) for e in result]

    def add_new_item_type(self, item_template):
        """ Add a new item type - just define the shape and the initial uses
            it will be added to the database
        :param item_template: An ItemTemplate PRefilled with Shape and IntialUses
        :return: an ItemTemplate Object with id set to the new id
        """
        result = self.item_service.add_new_item_type(item_template.name, item_template.shape, item_template.initial_uses)
        if result is not None:
            item_template.type_id = result
            return item_template
        else:
            return