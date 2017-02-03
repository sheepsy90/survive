# -*- coding:utf-8 -*-


class TiledScript():

    def __init__(self, script_id, properties):
        self.script_id = script_id

        assert u'script' in properties
        assert u'script_key' in properties

        self.script_params = {key: properties[key] for key in properties if u'script_' in key}

    def get_script_id(self):
        return self.script_id

    def get_script_parameters(self):
        return self.script_params

    @staticmethod
    def from_dict(dictionary):
        assert u'type' in dictionary
        assert u'properties' in dictionary

        properties = dictionary[u'properties']
        object_id = int(dictionary[u"type"])

        return TiledScript(object_id, properties)

