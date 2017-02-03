# -*- coding:utf-8 -*-

class Observable(object):

    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_all(self):
        for observer in self.observers:
            observer.notify()


class HealthModifierManager(Observable):

    def __init__(self):
        Observable.__init__(self)
        self.health_mods = {}
        self.marked_clear = False

    def update_health_mod(self, mod_type, amount):
        if self.marked_clear:
            self.health_mods = {}
            self.marked_clear = False
        self.health_mods[mod_type] = amount
        self.notify_all()

    def get_health_mods(self):
        return self.health_mods

    def clear_health_mods(self):
        self.marked_clear = True
