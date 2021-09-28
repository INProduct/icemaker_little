import json
import uos

import logger

class Config:
    def __init__(self):
        self.network = {}
        self.temperatures = {}
        self.times = {}


class ConfigParser:

    @classmethod
    def read_config(cls):
        cls.config = None
        if 'config.json' in uos.listdir():
            with open('config.json') as config_file:
                try:
                    cls.config = json.loads(config_file.read())
                    print(cls.config)
                except:
                    logger.Logger.write_error('can not read config file')
        else:
            cls._write_default_config()

    @classmethod
    def get_config_for(cls, key):
        return cls.config.get(key) if cls.config else None

    @classmethod
    def write_config(cls):
        pass  # todo write config  # todo depricated

    @classmethod
    def _write_default_config(cls):
        jsonfile = {
            'debug_level': 3,
            'network': {'enabled': False},
            'times': {
                'make_ice_period': 600000,
                'push_out_period': 50000,
            },
        }
        with open('config.json', 'w') as configfile:
            configfile.write(json.dumps(jsonfile))

