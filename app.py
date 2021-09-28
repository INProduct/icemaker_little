from machine import Pin, RTC, Timer
from time import time

from logger import Logger
from valve import Valve
from pump import Pump
from temperature_sensor import TemperatureSensor


class IceMakerStatus:
    ERROR = 0
    INIT = 1
    COOLING_DOWN = 2
    MAKE_ICE = 3
    PUSH_OUT = 4


class IceMaker:
    def __init__(self):
        self._status = IceMakerStatus.ERROR
        self.switch_status(IceMakerStatus.INIT)
        # TIMER AND TIMES
        self._work_timer = Timer(1)
        self._make_ice_period = 11 * 60 * 1000  # todo read from config
        self._push_out_period = 1 * 60 * 1000  # todo read from config
        # VALVES
        self._water_inlet_valve = Valve(Pin(10), True)  # todo Pinbelegung
        self._cooling_water_valve = Valve(Pin(10), True)  # todo Pinbelegung
        self._cooling_valve = Valve(Pin(10), True)  # todo Pinbelegung
        # PUMPS
        self._water_pump = Pump(Pin(10), True)  # todo Pinbelegung
        self._compressor = Pump(Pin(10), True)  # todo Pinbelegung
        # TEMPERATURES
        self._temperature_cooling = TemperatureSensor(Pin(10))  # todo Pinbelegung
        self._temperature_indoor = TemperatureSensor(Pin(10))  # todo Pinbelegung
        self._temperature_heater = TemperatureSensor(Pin(10))  # todo Pinbelegung
        self.temperatures = []
        self.temperatures.append(self._temperature_cooling)
        self.temperatures.append(self._temperature_indoor)
        self.temperatures.append(self._temperature_heater)

    def switch_status(self, status: IceMakerStatus):
        Logger.write_info('switch to ' + str(status) + 'status')
        self._status = status

    def set_error(self):
        Logger.write_error('Error')  # todo what kind of error
        self.switch_status(IceMakerStatus.ERROR)
        self._work_timer.deinit()
        self._switch_all_off()

    def _switch_all_off(self):
        self._compressor.switch_off()
        self._water_pump.switch_off()
        self._water_inlet_valve.switch_off()
        self._cooling_valve.switch_off()
        self._cooling_water_valve.switch_off()
        Logger.write_error('All switched off')

    def _cooling_down_handler(self):
        self._compressor.switch_on()

    def _make_ice_handler(self, t):
        self.switch_status(IceMakerStatus.MAKE_ICE)
        self._water_inlet_valve.switch_off()
        self._water_pump.switch_on()
        self._cooling_valve.switch_on()  # if switching on the valve make cold
        self._work_timer.init(mode=Timer.ONE_SHOT, period=1000, callback=self._push_out_handler)

    def _push_out_handler(self, t):
        self.switch_status(IceMakerStatus.PUSH_OUT)
        self._cooling_valve.switch_off()  # if switching off the valve make warm
        self._water_pump.switch_off()
        self._water_inlet_valve.switch_on()
        self._work_timer.init(mode=Timer.ONE_SHOT, period=1000, callback=self._make_ice_handler)

    def main_loop(self):
        while self._status > IceMakerStatus.ERROR:
            for temp in self.temperatures:
                res = temp.update()


