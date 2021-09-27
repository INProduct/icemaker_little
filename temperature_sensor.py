from machine import Pin
from onewire import OneWire
import DS18x20


class TempSensor:
    def __init__(self):
        pass


class TempManager:
    def __init__(self, pin: Pin):
        self._pin = pin
        self._ow = OneWire(self._pin)
        