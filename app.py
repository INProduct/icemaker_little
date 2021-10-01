from machine import Pin, Timer
import utime
from config_manager import ConfigParser
from signallampe import Signallampe
from logger import Logger
from valve import Valve
from pump import Pump
from temperature_sensor import TemperatureSensor, TemperatureKind
from icemaker_status import IceMakerStatus, IceMakerError

class IceMaker:
    def __init__(self):
        self._signallampe = Signallampe(Pin(23, Pin.OUT))
        self._status = IceMakerStatus.OFF
        self.switch_status(IceMakerStatus.INIT)
        # TIMER AND TIMES
        self._work_timer = Timer(1)
        self._make_ice_period = ConfigParser.get_config_for('times')['make_ice_period']
        self._push_out_period = ConfigParser.get_config_for('times')['push_out_period']
        # VALVES
        self._water_inlet_valve = Valve(Pin(14, Pin.OUT), True)
        self._cooling_water_valve = Valve(Pin(27, Pin.OUT), True)
        self._cooling_valve = Valve(Pin(26, Pin.OUT), True)
        # PUMPS
        self._water_pump = Pump(Pin(25, Pin.OUT), True)
        self._compressor = Pump(Pin(33, Pin.OUT), True, self._signallampe.set_compressor_light)

        # TEMPERATURSENSORS
        # todo dont forget make sensor Cold after tests
        self._temperature_indoor = TemperatureSensor('Indoor', Pin(15), TemperatureKind.HEAT,
                                                      ConfigParser.get_config_for('temperatures')['indoor'],
                                                      ConfigParser.get_config_for('temperatures')['indoor_hysterese'])
        self._temperature_cooling = TemperatureSensor('Cooling Zone', Pin(2), TemperatureKind.HEAT,
                                                      ConfigParser.get_config_for('temperatures')['cooling_zone'],
                                                      ConfigParser.get_config_for('temperatures')['cooling_zone_hysterese'])
        self._temperature_stb = TemperatureSensor('STB', Pin(4), TemperatureKind.COLD,
                                                      ConfigParser.get_config_for('temperatures')['stb'],
                                                      ConfigParser.get_config_for('temperatures')['stb_hysterese'])
        self.temperatures = []
        self.temperatures.append(self._temperature_cooling)
        self.temperatures.append(self._temperature_indoor)
        self.temperatures.append(self._temperature_stb)
        utime.sleep_ms(1000)
        self._read_temperatures()
        utime.sleep_ms(2000)
        self.switch_status(IceMakerStatus.COOLING_DOWN)

    def switch_status(self, status: IceMakerStatus):
        Logger.write_info('switch to ' + str(status) + ' status')
        if status == IceMakerStatus.READY_COOLING and not self._status == IceMakerStatus.READY_COOLING:
            self._work_timer.init(mode=Timer.ONE_SHOT, period=500, callback=self._push_out_handler)
        self._status = status
        self._signallampe.update(self._status)

    def set_error(self, msg: str, error: IceMakerError):
        self.switch_status(IceMakerStatus.ERROR)
        self._work_timer.deinit()
        self._switch_all_off()
        Logger.write_error('Error ' + msg)
        self._signallampe.set_error(error)

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
        self._cooling_valve.switch_off()
        self._work_timer.init(mode=Timer.ONE_SHOT, period=self._make_ice_period, callback=self._push_out_handler)

    def _push_out_handler(self, t):
        self.switch_status(IceMakerStatus.PUSH_OUT)
        self._water_pump.switch_off()
        self._water_inlet_valve.switch_on()
        self._cooling_valve.switch_on()
        self._work_timer.init(mode=Timer.ONE_SHOT, period=self._push_out_period, callback=self._make_ice_handler)

    def _read_temperatures(self):
        for temp in self.temperatures:
            if temp.update() == -1:
                self.set_error(temp.name, IceMakerError.TEMP_SENS)

    def main_loop(self):
        while self._status > IceMakerStatus.ERROR:
            self._signallampe.update(self._status)
            self._read_temperatures()
            # TEMPERATURE LOGIC
            if self._status == IceMakerStatus.COOLING_DOWN and self._temperature_indoor.status:
                self._compressor.switch_on()
            elif self._status == IceMakerStatus.COOLING_DOWN and not self._temperature_indoor.status:
                self._compressor.switch_off()
                self.switch_status(IceMakerStatus.READY_COOLING)

            if self._temperature_cooling.status:
                self._compressor.switch_on()
            else:
                self._compressor.switch_off()

            # STB LOGIC
            if self._status > IceMakerStatus.INIT and self._temperature_stb.status:
                print(self._temperature_stb.temperature)
                self.set_error('STB Compressor is hot', IceMakerError.STB)
        self._switch_all_off()
