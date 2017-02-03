from multiprocessing import Queue
import threading
import time
from common.ItemTemplate import ItemTemplate
from server.xmlrpc_services.crafting.CraftingPersistence import CraftingPersistence, CraftingPersistenceSqlQueueCommand


class CraftingService(threading.Thread):
    """ This is the service accessing the item types """

    def __init__(self, db_path="crafting.db"):
        threading.Thread.__init__(self)

        self.db_path = db_path

        self.persistence = CraftingPersistence(db_path)

        self.current_max_item_type_id = self.persistence.get_maximum_item_type_id()

        print "Startup Complete - Maximum Type Id is", self.current_max_item_type_id
        self.item_id_lock = threading.Lock()

        self.item_type_creation_queue = Queue()

        self.create_crafting_recipe = threading.Lock()

        self.item_template_cache = {}
        self.crafting_recipe_cache = {}

        self.start()

    def get_item_template(self, type_id):
        """ This method should access some kind of database to get the item template """
        if type_id in self.item_template_cache:
            return self.item_template_cache[type_id]
        else:
            item_template = self.persistence.load_item_type_from_database(type_id)
            if item_template is not None:
                self.item_template_cache[item_template.type_id] = item_template
            return item_template

    def get_item_types_by_drop_path_and_level(self, drop_path, level):
        return self.persistence.get_item_types_by_drop_path_and_level(drop_path, level)

    def get_crafting_recipe(self, crafting_representation):
        """ This method should access some kind of database to get the item template """
        if crafting_representation in self.crafting_recipe_cache:
            return self.crafting_recipe_cache[crafting_representation]
        else:
            crafting_recipe = self.persistence.get_crafting_recipe(crafting_representation)
            if crafting_recipe is not None:
                self.crafting_recipe_cache[crafting_representation] = crafting_recipe
            return crafting_recipe

    def get_incremented_item_type_id(self):
        self.item_id_lock.acquire()
        self.current_max_item_type_id += 1
        value = self.current_max_item_type_id
        self.item_id_lock.release()
        return value

    def process_crafting_request(self, crafting_representation):
        """ This method gets a string representation oft the recipe
            to find the result or to check if there is no such thing """
        if crafting_representation == "":
            return None

        if self.is_using_dummy_items(crafting_representation):
            return None

        crafting_recipe = self.get_crafting_recipe(crafting_representation)

        if crafting_recipe is None:
            return self.create_crafted_dummy(crafting_representation)
        else:
            if crafting_recipe.forbidden:
                return None
            else:
                results = crafting_recipe.results
                results = [[self.get_item_template(e[0]), e[1]] for e in results]
                return results

    def create_crafted_dummy(self, crafting_representation):
        """ This method calculates a unique id based on the recipe representation and gives that
            back as type id """
        self.create_crafting_recipe.acquire()

        craft_recipe = self.get_crafting_recipe(crafting_representation)

        if craft_recipe is not None:
            # Recipe already exists so we extract the type id
            new_type_id, count = craft_recipe.results[0]
            resulting_item_template = self.get_item_template(new_type_id)
        else:
            new_type_id = self.get_incremented_item_type_id()
            self.item_type_creation_queue.put(CraftingPersistenceSqlQueueCommand(CraftingPersistenceSqlQueueCommand.ITEM_TYPE_CREATION, [new_type_id, CraftingPersistence.DUMMY_TYPE_NAME, (1,1), 0]))
            self.item_type_creation_queue.put(CraftingPersistenceSqlQueueCommand(CraftingPersistenceSqlQueueCommand.CRAFTING_RECIPE_CREATION, [crafting_representation, False, [(new_type_id, 1)]]))
            resulting_item_template = ItemTemplate(CraftingPersistence.DUMMY_TYPE_NAME, "dummy/"+str(new_type_id), 0, new_type_id, (1, 1), 0, ItemTemplate.EMPTY_TAGS_STRING)
            # TODO Make sure that the crafting recipe is not delayed in written by the queue to the database and therefore the next crafting recipe is concurenting
            # Put it explicitly in the cache because the db could be to slow to save that until the next request comes
            self.item_template_cache[new_type_id] = resulting_item_template

        self.create_crafting_recipe.release()

        return [(resulting_item_template, 1)]

    def is_using_dummy_items(self, crafting_representation):
        type_set = set([int(e) for e in crafting_representation.replace('#', ';').split(";")])

        for type_id in type_set:
            if type_id == 0:
                continue
            if self.get_item_template(type_id).name == CraftingPersistence.DUMMY_TYPE_NAME:
                return True

        # TODO Make that more abstract - this currently a deal breaker for other types of crafting the elctronics
        if 18 in type_set and 19 in type_set and crafting_representation != "18;18;19#18;18;19":
            return True

        return False

    def run(self):
        persistence = CraftingPersistence(self.db_path)

        while True:
            pssqlqc = self.item_type_creation_queue.get()

            if pssqlqc.type == CraftingPersistenceSqlQueueCommand.CRAFTING_RECIPE_CREATION:
                crafting_representation, forbidden, result = pssqlqc.data
                persistence.save_crafting_recipe(crafting_representation, forbidden, "Dummy Crafting Recipe", result)
            elif pssqlqc.type == CraftingPersistenceSqlQueueCommand.ITEM_TYPE_CREATION:
                type_id, name, shape, initial_usages = pssqlqc.data
                persistence.save_item_template(type_id, name, shape, initial_usages)
            time.sleep(0.01)




