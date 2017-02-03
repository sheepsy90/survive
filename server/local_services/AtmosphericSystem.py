# -*- coding:utf-8 -*-


class AtmosphericSystem():

    HOSTILE = 1
    NORMAL = 0

    def __init__(self, temperature, atmospheric_type):
        self.temperature = temperature
        self.atmospheric_type = atmospheric_type

    def get_temperature(self):
        return self.temperature

    def get_atmospheric_type(self):
        return self.atmospheric_type
