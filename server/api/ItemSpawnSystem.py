# -*- coding:utf-8 -*-
import random
from server.setup.SearchGrouping import SearchGroupingManager


class ItemSpawnSystem():
    """
        This class is responsible for spawning new items if necessary - it looks at the searchable type
        attribute of a requested search area and builds up an item drop for that container
    """

    def __init__(self, item_service_client, crafting_service_client):
        self.item_service_client = item_service_client
        self.crafting_service_client = crafting_service_client

        self.available_searchable_types = SearchGroupingManager()

    @staticmethod
    def determine_percentage_of_drop_elements(drop_elements):
        chances_list = [d.drop_chance for d in drop_elements]

        total_chance = sum(chances_list)

        percentage_list = [e/float(total_chance) for e in chances_list]
        percentage_list = [e for e in percentage_list]
        return percentage_list

    def method_name(self, container, drop_element, items_in_container, items_in_category, percent_roll_prob):
        # Get the current drop element
        drop_path = drop_element.path
        drop_level = drop_element.level

        # Now we have a list of item templates
        item_type_list = self.crafting_service_client.get_item_types_by_drop_path_and_level(drop_path, drop_level)
        print "Item type list", item_type_list

        if len(item_type_list) == 0:
            return items_in_category

        # Generate a random number of things that shall go in this container
        num_items = items_in_category

        # Make the roll for the percentage value
        if random.random() < percent_roll_prob:
            num_items += 1

        print "Try to spawn", num_items, "items"
        # Build up a index list of the items to spawn
        item_types_to_spawn = [random.randint(0, len(item_type_list) - 1) for i in range(num_items)]
        print "Item Spawn index list", item_type_list
        for index in item_types_to_spawn:
            item_type = item_type_list[index]
            item = self.item_service_client.create_multiple_items(item_type, 1)[0]
            items_in_container.append(item)

            container.content = items_in_container
            if container.prepare_content() is None:
                # It doesn't worked so we need to delete the item
                item_to_delete = items_in_container[len(items_in_container) - 1]
                self.item_service_client.delete_item(item_to_delete.get_id())
                items_in_container = items_in_container[:len(items_in_container) - 1]
            else:
                print "Current List Stable - Count:", len(items_in_container)
        return items_in_container

    def handle_container(self, container):
        """
        :param container: A Container which shall be filled
        :return: True on success, False on an error
        """

        # First we get the searchable type
        searchable_type = container.get_searchable_type()

        # Then the corresponding SearchGroup
        search_group = self.available_searchable_types.get_search_grouping_by_name(searchable_type)

        if search_group is None:
            print "[ERROR] Could not found requested search group - %s not defined!" % searchable_type
            return False

        print "Search Group to spawn from", search_group

        # First we extract the shape from the grouping
        shape = search_group.get_size()
        container.shape = shape

        drop_elements = search_group.get_drop_element_list()
        n_items_min, n_items_max = search_group.get_number_items_to_spawn()
        num_items = random.randint(n_items_min, n_items_max)

        if len(drop_elements) > 1:
            # We have more than one DropElement so we need to determine their percentage occurrence
            print "[NOT IMPLEMENTED] More than 1 DropElement", self
            percentages = self.determine_percentage_of_drop_elements(drop_elements)
            percentages = [num_items*e for e in percentages]
            num_items_per_category = [int(e) for e in percentages]
            percentage_items_per_category = [e % 1 for e in percentages]

            assert len(num_items_per_category) == len(percentage_items_per_category)

            items_in_container = []

            for drop_element_index in range(len(drop_elements)):
                drop_element = drop_elements[drop_element_index]

                num_items_in_category = num_items_per_category[drop_element_index]
                percentage_roll_in_category = percentage_items_per_category[drop_element_index]

                items_in_container = self.method_name(container, drop_element, items_in_container,
                                                      num_items_in_category, percentage_roll_in_category)

            container.content = items_in_container
            assert container.prepare_content()
            print "Spawned", container.content
            return True

        elif len(drop_elements) == 1:
            # We need to handle exactly 1 drop element so we don't need to consider the probability
            drop_element = drop_elements[0]

            percentage_roll_in_category = 0

            items_in_container = []
            items_in_container = self.method_name(container, drop_element, items_in_container,
                                                  num_items, percentage_roll_in_category)

            container.content = items_in_container
            assert container.prepare_content()
            print "Spawned", container.content
            return True
        else:
            print "[ERROR] Could not generate items - no DropElements for %s!" % searchable_type
            return False
