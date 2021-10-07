class IceMakerStatus:
    OFF = 0
    ERROR = 1
    INIT = 2
    COOLING_DOWN = 3
    READY_COOLING = 4
    MAKE_ICE = 5
    PUSH_OUT = 6


class IceMakerError:
    NOERROR = -1
    UNRECOGNIZED = 0
    TEMP_SENS = 1
    OVERTIME = 2
    STB = 3


class IceMakerMode:
    OFF = 0
    CLEAN = 1
    HAND = 2
    AUTOMATIC = 3
