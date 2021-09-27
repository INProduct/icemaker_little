import os

import config_manager


class LogLevel:
    ERROR = 1
    WARNING = 2
    INFO = 3


class Logger:
    @classmethod
    def _write_log(cls, msg: str, log_level: LogLevel):
        errorlog_path = config_manager.ConfigParser.get_config_for('error_log')
        if not errorlog_path:
            errorlog_path = 'errorlog_path.csv'
        with open(errorlog_path, 'a') as errorlog:
            errorlog.write(msg + ', ' + log_level + ';')

    @classmethod
    def write_error(cls, msg: str):
        cls._write_log(str, LogLevel.ERROR)

    @classmethod
    def write_warning(cls, msg: str):
        cls._write_log(msg, LogLevel.WARNING)

    @classmethod
    def write_info(cls, msg: str):
        cls._write_log(msg, LogLevel.INFO)
