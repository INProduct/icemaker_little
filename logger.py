import os


class LogLevel:
    ERROR = 1
    WARNING = 2
    INFO = 3


class Logger:
    @classmethod
    def _write_log(cls, msg: str, log_level: LogLevel):
        pass # todo write log

    @classmethod
    def write_error(cls, msg: str):
        cls._write_log(str, LogLevel.ERROR)

    @classmethod
    def write_warning(cls, msg: str):
        cls._write_log(msg, LogLevel.WARNING)

    @classmethod
    def write_info(cls, msg: str):
        cls._write_log(msg, LogLevel.INFO)
