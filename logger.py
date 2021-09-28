import config_manager

# todo logrotate

class LogLevel:
    NONE = 0
    ERROR = 1
    WARNING = 2
    INFO = 3


class Logger:
    @classmethod
    def init(cls, debug_level: LogLevel = LogLevel.INFO):
        cls.debug_level = debug_level

    @classmethod
    def _write_log(cls, msg: str, log_level: LogLevel):
        log_path = config_manager.ConfigParser.get_config_for('logfile')
        if log_path is None:
            log_path = 'log.csv'
        with open(log_path, 'a') as log:
            log.write(msg + ', ' + str(log_level) + ';\n')

    @classmethod
    def write_error(cls, msg: str):
        print('Error: ', msg)
        if cls.debug_level > 0:
            cls._write_log(msg, LogLevel.ERROR)

    @classmethod
    def write_warning(cls, msg: str):
        print('Warning: ', msg)
        if cls.debug_level > 1:
            cls._write_log(msg, LogLevel.WARNING)

    @classmethod
    def write_info(cls, msg: str):
        print('Info: ', msg)
        if cls.debug_level > 2:
            cls._write_log(msg, LogLevel.INFO)
