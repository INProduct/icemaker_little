from machine import Pin
from onewire import OneWire
import ds18x20
import utime


class TemperatureSensor:
    def __init__(self, pin: Pin):
        self._pin = pin
        self._onewire = OneWire(self._pin)
        self._ds = ds18x20.DS18x20(self._onewire)
        self._roms = self._ds.scan()
        self._timeout = 750  # todo params
        self._next_time = utime.ticks_ms() + self._timeout

    @property
    def temperature(self):
        return self._temp

    def _get_temperature(self):
        self._ds.convert_temp()
        self._temp = self._ds.read_temp(self._roms[0])
        self._next_time = utime.ticks_ms() + self._timeout

    def update(self):
        if self._next_time < utime.ticks_ms():
            self._get_temperature()
