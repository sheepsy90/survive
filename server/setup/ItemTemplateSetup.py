# -*- coding:utf-8 -*-
import json

from common.ItemTemplateTags import ItemTemplateTags


class PathContext():

    def __init__(self, cursor, creation_manager_and_mapper, path):
        self.cursor = cursor
        self.creation_manager_and_mapper = creation_manager_and_mapper
        self.path = path

    def add_item_template(self, level, identifier, name, initial_uses, shape, image_path, tag_list):
        # Get a new unique id
        new_unique_id = self.creation_manager_and_mapper.get_unique_id()

        # Enter the Item at the CreationMapper
        self.creation_manager_and_mapper.add_to_image_mapping(new_unique_id, image_path)

        #TODO Expand the ItemTypeDB for identifier

        # Then try to put it into the database
        try:
            self.cursor.execute("INSERT INTO item_types VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [new_unique_id, self.path+identifier, level, name, tag_list, initial_uses, shape[0], shape[1]])
            self.creation_manager_and_mapper.log_item_type_created(new_unique_id, self.path, identifier, name, success=True)
        except Exception as e:
            self.creation_manager_and_mapper.log_item_type_created(new_unique_id, self.path, identifier, name, success=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class CreationManagerAndMapper():

    def __init__(self):
        self.unique_id = 1
        self.id_image_map = {}

    def get_unique_id(self):
        result = self.unique_id
        self.unique_id += 1
        return result

    def log_item_type_created(self, new_unique_id, path, identifier, name, success=True):
        print "DB-Written: %s\t%s: %s%s - %s" % (success, str(new_unique_id), path, identifier, name, )

    def add_to_image_mapping(self, unique_id, image_path):
        self.id_image_map[unique_id] = image_path

    def write_files(self):
        with open("id_image_mapping.json", "w") as f:
            f.write(json.dumps(self.id_image_map))


class ItemTemplateSetup():

    def __init__(self, cursor):
        self.cursor = cursor
        self.cmam = CreationManagerAndMapper()

    def setup(self):

        with PathContext(self.cursor, self.cmam, "item/food/fruits/") as pc:
            pc.add_item_template(1, "citrus", "Zitrone", 3, (1, 2), "items/citrus", ItemTemplateTags.from_list(
                ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "potato", "Kartoffel", 3, (1, 2), "items/potato", ItemTemplateTags.from_list(
                ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "apple", "Apfel", 3, (1, 2), "items/apple", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "cucumber", "Gurke", 3, (1, 2), "items/cucumber", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "banana", "Banane", 3, (1, 2), "items/banana", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))

        with PathContext(self.cursor, self.cmam, "item/food/spices/") as pc:
            pc.add_item_template(1, "salt", "Salt", 3, (1, 2), "items/salt", ItemTemplateTags.from_list())
            pc.add_item_template(1, "pepper", "Pepper", 3, (1, 2), "items/pepper", ItemTemplateTags.from_list())

        with PathContext(self.cursor, self.cmam, "item/food/snacks/") as pc:
            pc.add_item_template(1, "chocolate_bar", "Chocolate Bar", 3, (2, 1), "items/chocolate_bar", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "cereal_bar", "Cereal Bar", 3, (2, 1), "items/cereal_bar", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "cracker", "Cracker", 3, (2, 2), "items/cracker", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "cookies", "Cookies", 3, (2, 2), "items/cookies", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))
            pc.add_item_template(1, "marshmallow", "Marshmallow", 3, (2, 2), "items/marshmallow", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_FOOD,
            ))

        with PathContext(self.cursor, self.cmam, "item/food/prepared_foods/") as pc:
            pc.add_item_template(1, "canned_tuna", "Canned Tuna", 3, (1, 2), "items/pepper", ItemTemplateTags.from_list())
            pc.add_item_template(1, "canned_spaghetti", "Canned Spaghetti", 3, (1, 2), "items/pepper", ItemTemplateTags.from_list())

        with PathContext(self.cursor, self.cmam, "item/drink/bottles/") as pc:
            pc.add_item_template(1, "water_bottle", "Water Bottle", 3, (1, 2), "items/water_bottle", ItemTemplateTags.from_list(
                 ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_DRINK,
            ))

        with PathContext(self.cursor, self.cmam, "item/weapons/axe/") as pc:
            pc.add_item_template(1, "fire_axe", "Axe", 0, (2, 3), "items/fire_axe", ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND))

        with PathContext(self.cursor, self.cmam, "item/equipment/mask/armor/") as pc:
            pc.add_item_template(1, "atmospheric_mask", "Atmospheric Mask", 60, (2, 2), "items/atmospheric_mask", ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE, ItemTemplateTags.MASK, ItemTemplateTags.AUTO_CONSUMES_ON_BAD_ATMOSPHERE))

        with PathContext(self.cursor, self.cmam, "item/electronics/components/") as pc:
            pc.add_item_template(1, "electrical_component_a", "Electrical Component A", 0, (2, 2), "items/electrical_component_a", ItemTemplateTags.from_list())
            pc.add_item_template(1, "electrical_component_b", "Electrical Component B", 0, (2, 1), "items/electrical_component_b", ItemTemplateTags.from_list())
            pc.add_item_template(1, "electrical_component_ab", "Electrical Component AB", 0, (2, 3), "items/electrical_component_ab", ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.COMPONENT_AB))

        with PathContext(self.cursor, self.cmam, "item/medical/basics/") as pc:
            pc.add_item_template(1, "bandage", "Bandage", 1, (1, 1), "items/bandage", ItemTemplateTags.from_list())
            pc.add_item_template(1, "painkiller_pills", "Painkiller Pills", 8, (4, 2), "items/painkiller_pills", ItemTemplateTags.from_list())
            pc.add_item_template(2, "anti_poison_pills", "Anti-Poison Pills", 6, (3, 2), "items/anti_poison_pills", ItemTemplateTags.from_list())
            pc.add_item_template(2, "anti_nausea_pills", "Anti-Nausea Pills", 6, (3, 2), "items/anti_nausea_pills", ItemTemplateTags.from_list())

        self.setup_cards()

        # Please add new items after that so that the ids are not changed
        with PathContext(self.cursor, self.cmam, "item/medical/basics/") as pc:
            pc.add_item_template(2, "cooling_pad", "Cooling Pad", 1, (1, 1), "items/cooling_pad", ItemTemplateTags.from_list())
            pc.add_item_template(2, "syringe", "Syringe", 1, (2, 3), "items/syringe", ItemTemplateTags.from_list())

            pc.add_item_template(3, "morphin_injector", "Morphin Injector", 1, (3, 1), "items/morphin_injector", ItemTemplateTags.from_list())
            pc.add_item_template(3, "epinephrine_injector", "Epinephrine injector", 1, (3, 1), "items/epinephrine_injector", ItemTemplateTags.from_list())
            pc.add_item_template(3, "nosedrops", "Nose Drops", 30, (1, 2), "items/nosedrops", ItemTemplateTags.from_list())
            pc.add_item_template(3, "caffeine_pills", "Caffeine Pills", 15, (1, 2), "items/caffeine_pills", ItemTemplateTags.from_list())

            pc.add_item_template(4, "insulin", "Insulin", 1, (3, 2), "items/insulin", ItemTemplateTags.from_list())

        with PathContext(self.cursor, self.cmam, "item/drink/bottles/") as pc:
            pc.add_item_template(1, "lemonade", "Lemonade", 3, (1, 2), "items/lemonade", ItemTemplateTags.from_list(
                     ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.WEAPON
            ))
            pc.add_item_template(1, "milk", "Milk", 3, (1, 2), "items/milk", ItemTemplateTags.from_list(
                     ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_DRINK,
            ))
            pc.add_item_template(1, "chocolate_milk", "Chocolate Milk", 3, (1, 2), "items/chocolate_milk", ItemTemplateTags.from_list(
                     ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_DRINK,
            ))
            pc.add_item_template(1, "strawberry_milk", "Strawberry Milk", 3, (1, 2), "items/strawberry_milk", ItemTemplateTags.from_list(
                     ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_DRINK,
            ))
            pc.add_item_template(1, "energy_drink", "Energy Drink", 3, (1, 2), "items/energy_drink", ItemTemplateTags.from_list(
                     ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_DRINK,
            ))
            pc.add_item_template(1, "bitter_lemon", "Bitter Lemon", 3, (1, 2), "items/bitter_lemon", ItemTemplateTags.from_list(
                     ItemTemplateTags.WEARABLE, ItemTemplateTags.HAND, ItemTemplateTags.CONSUMABLE, ItemTemplateTags.CONSUMES_AS_DRINK,
            ))

        self.cmam.write_files()

    def setup_cards(self):
        with PathContext(self.cursor, self.cmam, "item/equipment/id_card/") as pc:
            pc.add_item_template(1, "id_card_0000", "ID-Card (Sec.0, Tec.0, Adm.0, Sci.0)", 0, (3, 2), "items/id_cards/id_card_0_0_0_0",
                                 ItemTemplateTags.from_list(ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE,
                                                          ItemTemplateTags.HAND)))

            pc.add_item_template(1, "id_card_1000", "ID-Card (Sec.1, Tec.0, Adm.0, Sci.0)", 0, (3, 2), "items/id_cards/id_card_1_0_0_0",
                                 ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE,
                                                          ItemTemplateTags.HAND,
                                                          ItemTemplateTags.SECURITY_1))

            pc.add_item_template(1, "id_card_0100", "ID-Card (Sec.0, Tec.1, Adm.0, Sci.0)", 0, (3, 2), "items/id_cards/id_card_0_1_0_0",
                                 ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE,
                                                          ItemTemplateTags.HAND,
                                                          ItemTemplateTags.TECHNICIAN_1))

            pc.add_item_template(1, "id_card_0010", "ID-Card (Sec.0, Tec.0, Adm.1, Sci.0)", 0, (3, 2), "items/id_cards/id_card_0_0_1_0",
                                 ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE,
                                                          ItemTemplateTags.HAND,
                                                          ItemTemplateTags.ADMINISTRATION_1))

            pc.add_item_template(1, "id_card_0001", "ID-Card (Sec.0, Tec.0, Adm.0, Sci.1)", 0, (3, 2), "items/id_cards/id_card_0_0_0_1",
                                 ItemTemplateTags.from_list(ItemTemplateTags.WEARABLE,
                                                          ItemTemplateTags.HAND,
                                                          ItemTemplateTags.SCIENCE_1))

if __name__ == "__main__":
    it = ItemTemplateSetup(None)
    it.setup()