from machine import Pin, RTC
from time import time
from valve import Valve
from pump import Pump



class IceMaker:
    def __init__(self):
        self._water_inlet_valve = Valve(Pin(10), True) # todo Pinbelegung
        self._cooling_water_valve = Valve(Pin(10), True) # todo Pinbelegung
        self._cooling_valve = Valve(Pin(10), True) # todo Pinbelegung

        self._water_pump = Pump(Pin(10), True) # todo Pinbelegung
        self._compressor = Pump(Pin(10), True) # todo Pinbelegung


