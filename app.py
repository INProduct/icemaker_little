from machine import Pin, Timer
import utime
import json
from config_manager import ConfigParser
from signallampe import Signallampe
from logger import Logger
from valve import Valve
from pump import Pump
from temperature_sensor import TemperatureSensor, TemperatureKind
from icemaker_status import IceMakerStatus, IceMakerError, IceMakerMode

class IceMaker:
    def __init__(self):
        self._signallampe = Signallampe(Pin(23, Pin.OUT))
        self._status = IceMakerStatus.OFF
        self._mode = IceMakerMode.AUTOMATIC
        self._run = True
        self._last_switch_status_time = utime.time()
        self.switch_status(IceMakerStatus.INIT)
        self._error = IceMakerError.NOERROR
        # TIMER AND TIMES
        self._work_timer = Timer(1)

        self._make_ice_period = ConfigParser.get_config_for('times')['make_ice_period']
        self._push_out_period = ConfigParser.get_config_for('times')['push_out_period']
        # VALVES
        self._water_inlet_valve = Valve(Pin(14, Pin.OUT), False)
        self._fan = Valve(Pin(27, Pin.OUT), False)
        # PUMPS
        self._water_pump = Pump(Pin(26, Pin.OUT), False)
        self._compressor = Pump(Pin(25, Pin.OUT), False)

        # TEMPERATURSENSORS
        # todo dont forget make sensor Cold after tests
        self._temperature_indoor = TemperatureSensor('Indoor', Pin(15), TemperatureKind.COLD,
                                                      ConfigParser.get_config_for('temperatures')['indoor'],
                                                      ConfigParser.get_config_for('temperatures')['indoor_hysterese'])
        self._temperature_cooling = TemperatureSensor('Cooling Zone', Pin(2), TemperatureKind.COLD,
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

    def get_info(self):
        info = {}
        info['status'] = self._status
        info['error'] = self._error
        info['mode'] = self._mode
        info['temperatures'] = {
            'indoor': self._temperature_indoor.temperature,
            'cooling': self._temperature_cooling.temperature,
            'stb': self._temperature_stb.temperature,
            'indoor_status': self._temperature_indoor.status,
            'cooling_status': self._temperature_cooling.status,
            'stb_status': self._temperature_stb.status
        }
        info['last_switch_time'] = self._last_switch_status_time
        info['components'] = {
            'water_inlet': self._water_inlet_valve.get_status(),
            'compressor': self._compressor.get_status(),
            'fan': self._fan.get_status(),
            'pump': self._water_pump.get_status()
        }
        return json.dumps(info)

    def get_status(self):
        return self._status

    def switch_status(self, status: IceMakerStatus):
        Logger.write_info('switch to ' + str(status) + ' status')
        if status == IceMakerStatus.READY_COOLING and not self._status == IceMakerStatus.READY_COOLING:
            self._work_timer.init(mode=Timer.ONE_SHOT, period=500, callback=self._make_ice_handler)
        self._status = status
        self._signallampe.update(self._status)
        self._last_switch_status_time = utime.time()

    def switch_mode(self, mode: IceMakerMode):
        if not self._mode == mode:
            self._work_timer.deinit()
            self._switch_all_off()
            self._mode = mode
            self._run = False

    def hand_toggle_water_valve(self):
        if self._mode == IceMakerMode.HAND:
            self._water_inlet_valve.toggle()

    def hand_toggle_water_pump(self):
        if self._mode == IceMakerMode.HAND:
            self._water_pump.toggle()

    def hand_toggle_compressor(self):
        if self._mode == IceMakerMode.HAND:
            self._compressor.toggle()
            self._fan.toggle()

    def clean_start(self):
        if self._mode == IceMakerMode.CLEAN:
            self._run = True

    def clean_stop(self):
        if self._mode == IceMakerMode.CLEAN:
            self._run = False

    def automatic_start(self):
        if self._mode == IceMakerMode.AUTOMATIC:
            self.switch_status(IceMakerStatus.COOLING_DOWN)

    def automatic_stop(self):
        if self._mode == IceMakerMode.AUTOMATIC:
            self.switch_status(IceMakerStatus.OFF)

    def set_error(self, msg: str, error: IceMakerError):
        self.switch_status(IceMakerStatus.ERROR)
        self._work_timer.deinit()
        self._switch_all_off()
        Logger.write_error('Error ' + msg)
        self._error = error
        self._signallampe.set_error(error)

    def _switch_all_off(self):
        self._compressor.switch_off()
        self._water_pump.switch_off()
        self._water_inlet_valve.switch_off()
        self._fan.switch_off()

    def _make_ice_handler(self, t):
        self.switch_status(IceMakerStatus.MAKE_ICE)
        self._work_timer.init(mode=Timer.ONE_SHOT, period=ConfigParser.get_config_for('times')['make_ice_period'], callback=self._push_out_handler)

    def _push_out_handler(self, t):
        self.switch_status(IceMakerStatus.PUSH_OUT)
        self._work_timer.init(mode=Timer.ONE_SHOT, period=ConfigParser.get_config_for('times')['push_out_period'], callback=self._cooling_down_handler)

    def _cooling_down_handler(self, t):
        self.switch_status(IceMakerStatus.COOLING_DOWN)


    def _read_temperatures(self):
        for temp in self.temperatures:
            if temp.update() == -1:
                self.set_error(temp.name, IceMakerError.TEMP_SENS)

    def main_loop(self):
        while self._status > IceMakerStatus.ERROR:
            self._signallampe.update(self._status)
            self._read_temperatures()

            # MODES
            if self._mode == IceMakerMode.CLEAN and self._run:
                self._water_pump.switch_on()
            elif self._mode == IceMakerMode.CLEAN and not self._run:
                self._water_pump.switch_off()
            if self._mode == IceMakerMode.AUTOMATIC:
                # TEMPERATURE LOGIC
                if self._status == IceMakerStatus.COOLING_DOWN:
                    if self._temperature_indoor.status:
                        self._water_inlet_valve.switch_off()
                        self._water_pump.switch_on()
                        self._fan.switch_on()
                        self._compressor.switch_on()
                    elif not self._temperature_indoor.status:
                        self.switch_status(IceMakerStatus.READY_COOLING)

                if self._status == IceMakerStatus.MAKE_ICE:
                    self._water_inlet_valve.switch_off()
                    self._water_pump.switch_on()
                    if self._temperature_cooling.status:
                        self._compressor.switch_on()
                        self._fan.switch_on()
                    elif not self._temperature_cooling.status:
                        self._compressor.switch_off()

                elif self._status == IceMakerStatus.PUSH_OUT:
                    self._compressor.switch_off()
                    self._water_pump.switch_off()
                    self._water_inlet_valve.switch_on()


            # STB LOGIC
            if self._status > IceMakerStatus.INIT and self._temperature_stb.status:
                print(self._temperature_stb.temperature)
                self.set_error('STB Compressor is hot', IceMakerError.STB)
        self._switch_all_off()
