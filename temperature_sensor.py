from machine import Pin
from onewire import OneWire, OneWireError
import ds18x20
import utime

from logger import Logger


class TemperatureKind:
    HEAT = 1
    COLD = 2

class TemperatureSensor:
    def __init__(self, pin: Pin, kind: TemperatureKind, switchpoint: int, hysterese: int):
        self._status = False
        self._pin = pin
        self._kind = kind
        self._temp = 0
        self._switchpoint = switchpoint
        self._hysterese = hysterese
        self._onewire = OneWire(self._pin)
        self._ds = ds18x20.DS18X20(self._onewire)
        self._roms = self._ds.scan()
        self._timeout = 750  # todo read from params
        self._next_time = utime.ticks_ms() + self._timeout
        Logger.write_info('Init Temperaturesensor '
                          + str(self._kind) + ' ' + str(self._switchpoint) + ' ' + str(self._hysterese))

    @property
    def temperature(self):
        return self._temp

    @property
    def status(self):
        return self._status

    def _get_temperature(self):
        self._ds.convert_temp()
        self._temp = self._ds.read_temp(self._roms[0])
        self._next_time = utime.ticks_ms() + self._timeout

    def update(self):
        if self._next_time < utime.ticks_ms():
            try:
                self._get_temperature()
            except OneWireError as e:
                Logger.write_error('Temperature sensor is broken' + str(e))
                return -1

            if self._kind == TemperatureKind.HEAT and self.temperature < self._switchpoint - self._hysterese:
                self._status = True
            elif self._kind == TemperatureKind.COLD and self.temperature > self._switchpoint + self._hysterese:
                self._status = True
            else:
                self._status = False

        return self._status

