from machine import Pin
from logger import Logger


class Pump:
    def __init__(self, pin: Pin, low_level: bool, callback=None):
        self._out = pin
        self._low_level = low_level
        self._callback = callback
        self.switch_off()
        Logger.write_info('Pump was init')

    def switch_off(self):
        self._out.value(self._low_level)
        self._trigger_callback()

    def switch_on(self):
        self._out.value(not self._low_level)
        self._trigger_callback()
        print('switched on')


    def toggle(self):
        self._out.value(not self._out.value())
        self._trigger_callback()

    def get_status(self):
        return True if self._out.value() and not self._low_level else False

    def _trigger_callback(self):
        if self._callback:
            self._callback(self.get_status())