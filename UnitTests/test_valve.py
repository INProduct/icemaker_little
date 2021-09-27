import unittest
from valve import Valve
from machine import Pin

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.valve_ll = Valve(Pin(22), True)
        self.valve_hl = Valve(Pin(22), False)

    def test_bevor_run_low_level(self):
        out_status = self.valve_ll._out.value()
        status = self.valve_ll.get_status()
        self.assertEqual(out_status, True)  # add assertion here
        self.assertEqual(status, False)

    def test_valve_on_low_level(self):
        self.valve_ll.switch_on()
        out_status = self.valve_ll._out.value()
        status = self.valve_ll.get_status()
        self.assertEqual(out_status, False)  # add assertion here
        self.assertEqual(status, True)

    def test_valve_off_low_level(self):
        self.valve_ll.switch_off()
        out_status = self.valve_ll._out.value()
        status = self.valve_ll.get_status()
        self.assertEqual(out_status, True)  # add assertion here
        self.assertEqual(status, False)

    def test_bevor_run_high_level(self):
        out_status = self.valve_ll._out.value()
        status = self.valve_ll.get_status()
        self.assertEqual(out_status, False)  # add assertion here
        self.assertEqual(status, False)

    def test_valve_on_high_level(self):
        self.valve_ll.switch_on()
        out_status = self.valve_ll._out.value()
        status = self.valve_ll.get_status()
        self.assertEqual(out_status, True)  # add assertion here
        self.assertEqual(status, True)

    def test_valve_off_high_level(self):
        self.valve_ll.switch_off()
        out_status = self.valve_ll._out.value()
        status = self.valve_ll.get_status()
        self.assertEqual(out_status, False)  # add assertion here
        self.assertEqual(status, False)


if __name__ == '__main__':
    unittest.main()
