# -*- coding:utf-8 -*-


class SimulationStepBufferQueue():

    WORLD_OBJECTS_DELETED = 4
    WORLD_OBJECTS_CHANGED = 3
    PLAYER_UPDATE = 2
    PLAYER_LEFT_AREA = 1

    def __init__(self, identifier):
        self.identifier = identifier
        self.queue = []

    def push(self, element):
        self.queue.append(element)

    def get_queue_content(self):
        return self.queue

    def clear(self):
        self.queue = []


class SimulationStepBufferQueueSystem():
    """ This is a general class which allows the functionality to register a queue via a specific identifier.
        It then allows to push objects into such a named queue and read the items and clear the queue afterwards.
        This method is needed for several parts of the application."""

    def __init__(self):
        self.queue_dictionary = {}

    def register(self, name):
        assert name not in self.queue_dictionary
        self.queue_dictionary[name] = SimulationStepBufferQueue(name)

    def push(self, name, element):
        assert name in self.queue_dictionary
        self.queue_dictionary[name].push(element)

    def get_queue_content(self, name):
        assert name in self.queue_dictionary
        return self.queue_dictionary[name].get_queue_content()

    def clear(self, name):
        assert name in self.queue_dictionary
        self.queue_dictionary[name].clear()

    def clear_all(self):
        for element in self.queue_dictionary.values():
            element.clear()

    def get_queue(self, name):
        assert name in self.queue_dictionary
        return self.queue_dictionary[name]