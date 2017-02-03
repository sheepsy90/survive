# -*- coding:utf-8 -*-
import json
import os


class Configuration():

    def __init__(self):
        self.conf_path = "/import/survive/config.json"

        value = os.environ.get("CONFIGURATION_PATH", None)

        if value is not None:
            self.conf_path = value

        self.configuration = self._load_config()

    def _load_config(self):
        with open(self.conf_path, 'r') as f:
            config = json.loads(f.read())
        return config

    def get_configuration(self):
        return self.configuration
