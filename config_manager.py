import json
import uos

import logger


class ConfigParser:

    @classmethod
    def read_config(cls):
        cls.config = None
        if 'config.json' in uos.listdir():
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
        return cls.config.get(key) if cls.config else None

    @classmethod
    def write_config(cls):
        pass  # todo write config
