from machine import Pin, Timer
from config_manager import ConfigParser

from logger import Logger
from valve import Valve
from pump import Pump
from temperature_sensor import TemperatureSensor, TemperatureKind


class IceMakerStatus:
    ERROR = 0
    INIT = 1
    COOLING_DOWN = 2
    READY_COOLING = 3
    MAKE_ICE = 4
    PUSH_OUT = 5


class IceMaker:
    def __init__(self):
        self._status = IceMakerStatus.ERROR
        self.switch_status(IceMakerStatus.INIT)
        # TIMER AND TIMES
        self._work_timer = Timer(1)
        self._make_ice_period = ConfigParser.get_config_for('times')['make_ice_period']
        self._push_out_period = ConfigParser.get_config_for('times')['push_out_period']
        # VALVES
        self._water_inlet_valve = Valve(Pin(12, Pin.OUT), True)
        self._cooling_water_valve = Valve(Pin(14, Pin.OUT), True)
        self._cooling_valve = Valve(Pin(27, Pin.OUT), True)
        # PUMPS
        self._water_pump = Pump(Pin(26, Pin.OUT), True)
        self._compressor = Pump(Pin(25, Pin.OUT), True)
        # TEMPERATURSENSORS
        self._temperature_indoor = TemperatureSensor('Indoor', Pin(2), TemperatureKind.HEAT,
                                                      ConfigParser.get_config_for('temperatures')['indoor'],
                                                      ConfigParser.get_config_for('temperatures')['indoor_hysterese'])
        self._temperature_cooling = TemperatureSensor('Cooling Zone', Pin(15), TemperatureKind.HEAT,
                                                      ConfigParser.get_config_for('temperatures')['cooling_zone'],
                                                      ConfigParser.get_config_for('temperatures')['cooling_zone_hysterese'])
        self.temperatures = []
        self.temperatures.append(self._temperature_cooling)
        self.temperatures.append(self._temperature_indoor)
        self.switch_status(IceMakerStatus.COOLING_DOWN)

    def switch_status(self, status: IceMakerStatus):
        Logger.write_info('switch to ' + str(status) + ' status')
        if status == IceMakerStatus.READY_COOLING and not self._status == IceMakerStatus.READY_COOLING:
            self._work_timer.init(mode=Timer.ONE_SHOT, period=500, callback=self._push_out_handler)
        self._status = status

    def set_error(self, msg: str):
        self._work_timer.deinit()
        self._switch_all_off()
        Logger.write_error('Error ' + msg)
        self.switch_status(IceMakerStatus.ERROR)

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
        self._work_timer.init(mode=Timer.ONE_SHOT, period=self._make_ice_period, callback=self._push_out_handler)

    def _push_out_handler(self, t):
        self.switch_status(IceMakerStatus.PUSH_OUT)
        self._water_pump.switch_off()
        self._water_inlet_valve.switch_on()
        self._work_timer.init(mode=Timer.ONE_SHOT, period=self._push_out_period, callback=self._make_ice_handler)

    def main_loop(self):
        while self._status > IceMakerStatus.ERROR:
            for temp in self.temperatures:
                if temp.update() == -1:
                    self.set_error(temp.name)
            # TEMPERATURE LOGIC
            if self._temperature_indoor.status:
                self._compressor.switch_on()
                self._cooling_valve.switch_on()
            else:
                self._compressor.switch_off()
                self._cooling_valve.switch_off()
                if self._status == IceMakerStatus.COOLING_DOWN:
                    self.switch_status(IceMakerStatus.READY_COOLING)
