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
        val = cls.config.get(key) if cls.config else None
        if not val:
            logger.Logger.write_error('No value for ' + str(key) + ' found')
        return val

    @classmethod
    def write_config(cls):
        with open('config.json', 'w') as configfile:
            configfile.write(json.dumps(cls.config))

    @classmethod
    def _write_default_config(cls):
        jsonfile = {
            'debug_level': 3,
            'network': {'enabled': False},
            'times': {
                'make_ice_period': 600000,
                'push_out_period': 50000,
                'tempsens_timeout_reads': 750,
            },
            'temperatures': {
                'indoor': -2,
                'indoor_hysterese': 2,
                'cooling_zone': -5,
                'cooling_zone_hysterese': 2,
                'stb': 70,
                'stb_hysterese': 2,
            },
            'signal': {
                'length': 1,
                'status': {
                    0: [0, 0, 0],
                    1: [255, 0, 0],
                    2: [125, 125, 0],
                    3: [0, 0, 255],
                    4: [0, 125, 255],
                    5: [100, 0, 255],
                    6: [125, 125, 0],
                },
                'error': {
                    0: 500,
                    1: 1000,
                    2: 2000,
                    3: 3000,
                }

            }

        }
        with open('config.json', 'w') as configfile:
            configfile.write(json.dumps(jsonfile))

