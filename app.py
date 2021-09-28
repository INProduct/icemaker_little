from machine import Pin, RTC
from time import time
from valve import Valve
from pump import Pump


class IceMakerStatus:
    ERROR = 0
    COOLING_DOWN = 1
    READY = 2
    WORK = 3


class IceMaker:
    def __init__(self):
        self._status = IceMakerStatus.INIT

        self._water_inlet_valve = Valve(Pin(10), True) # todo Pinbelegung
        self._cooling_water_valve = Valve(Pin(10), True) # todo Pinbelegung
        self._cooling_valve = Valve(Pin(10), True) # todo Pinbelegung

        self._water_pump = Pump(Pin(10), True) # todo Pinbelegung
        self._compressor = Pump(Pin(10), True) # todo Pinbelegung


