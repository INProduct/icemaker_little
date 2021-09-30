class IceMakerStatus:
    OFF = 0
    ERROR = 1
    INIT = 2
    COOLING_DOWN = 3
    READY_COOLING = 4
    MAKE_ICE = 5
    PUSH_OUT = 6


class IceMakerError:
    UNRECOGNIZED = 0
    TEMP_SENS = 1
    OVERTIME = 2