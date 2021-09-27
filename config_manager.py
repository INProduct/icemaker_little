import json
import os

import logger


class ConfigParser:

    @classmethod
    def read_config(cls):
        if os.path.exists('config.json'):
            with open('config.json') as config_file:
                try:
                    cls.config = json.loads(config_file.read())
                except:
                    logger.Logger.write_error('can not read config file')
        else:
            # todo create config or raise Exception
            pass

    @classmethod
    def get_config_for(cls, key):
        return cls.config.get(key)

    @classmethod
    def write_config(cls):
        pass  # todo write config
