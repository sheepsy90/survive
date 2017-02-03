# -*- coding:utf-8 -*-
import time


class PersistableComponent(object):

    def __init__(self):
        self.last_time_persisted = time.time()
        self.persistence_interval = 5

    def needs_persistence(self):
        return time.time() > self.last_time_persisted + self.persistence_interval

    def touch_last_time_persisted(self):
        self.last_time_persisted = time.time()