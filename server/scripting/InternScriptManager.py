# -*- coding:utf-8 -*-
import logging
import time
from server.constants.constans import INTERNAL_SCRIPT_MAPPING


logger = logging.getLogger(__name__)


class InternScriptManager(object):

    def __init__(self, level_identifier):
        self.level_identifier = level_identifier

        # GameObject related stuff
        self.scripts = {}

        self.components_cache = {}

        self.scheduled_scripts = []

    def add_script(self, script):
        """ This methods adds a kind of object to the map which can be in various states and so on - its
            almost surely represented by a tile within the client but we don't really need that here in the
            server """
        if script.get_script_id() not in self.scripts:
            self.scripts[script.get_script_id()] = script
        else:
            raise KeyError("Script Id is already used in another Element")

    def get_script(self, script_id):
        return self.scripts[script_id]

    def build_internal_scripts(self, server_level, tiled_scripts):

        for tiled_script in tiled_scripts:

            script_id = tiled_script.get_script_id()
            script_params = tiled_script.get_script_parameters()
            script_key = script_params[u'script_key']
            parameters = {key.split("_")[2]: script_params[key] for key in script_params if u'script_param_' in key}

            if script_key not in INTERNAL_SCRIPT_MAPPING:
                raise KeyError("Could not find {} in the internal script mappings.".format(script_key))

            initialized_script = INTERNAL_SCRIPT_MAPPING.get(script_key)(script_id, parameters, server_level)
            logger.info("Created Script: {}".format(initialized_script))

            # Add the object which implicitly also updates the Components Cache
            self.add_script(initialized_script)

    def initialize_scripts(self):
        for element in self.scripts.values():
            element.initialize()

    def schedule_script_call(self, script_schedule):
        self.scheduled_scripts.append(script_schedule)

    def resolve_script_schedule(self):
        current_time = time.time()
        to_execute = [e for e in self.scheduled_scripts if e.execution_time <= current_time]
        keep = [e for e in self.scheduled_scripts if e.execution_time > current_time]
        self.scheduled_scripts = keep

        for element in to_execute:
            self.get_script(element.script_id).handle_event(None, None)
