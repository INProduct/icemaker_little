from machine import Pin

from logger import Logger


class Pump:
    def __init__(self, pin: Pin, low_level: bool):
        self._out = pin
        self._low_level = low_level
        self.switch_off()
        Logger.write_info('Pump was init')

    def switch_off(self):
        self._out.value(self._low_level)

    def switch_on(self):
        self._out.value(not self._low_level)

    def toggle(self):
        self._out.value(not self._out.value())

    def get_status(self):
        return True if self._out.value() and not self._low_level else False
