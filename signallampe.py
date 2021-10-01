from machine import Pin, Timer
from neopixel import NeoPixel
from icemaker_status import IceMakerStatus
from config_manager import ConfigParser


class Signallampe:
    def __init__(self, pin: Pin):
        self._pin = pin
        self._length = ConfigParser.get_config_for('signal')['length']
        self._np = NeoPixel(self._pin, self._length)
        self._np[0] = (255, 255, 255)
        self._np.write()
        self._work_timer = Timer(3)
        self._last_status = IceMakerStatus.OFF

    def _set_color(self, status):
        for l in range(self._length):
            r, g, b = tuple(ConfigParser.get_config_for('signal')['status'][str(status)])
            self._np[l] = (r, g, b)
            self._np.write()

    def set_error(self, error):  # todo class error
        duration = ConfigParser.get_config_for('signal')['error'][str(error)]
        self._work_timer.init(mode=Timer.PERIODIC, period=duration, callback=self._error_light_toggle)

    def _error_light_toggle(self, t):
        r, g, b = self._np[0]
        if r == 0:
            self._set_color(1)
        else:
            self._set_color(0)

    def update(self, status: IceMakerStatus):
        if status is not self._last_status:
            self._last_status = status
            self._set_color(status)

