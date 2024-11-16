# Sensor for traffic count, using a PIO (e.g. reed or hall sensor)
import micropython
from machine import Pin

class Traffic:
    def __init__(self, pin_number: int):
        self._counter : int = 0
        self._pin = Pin(pin_number, Pin.IN)
        self._old_value = self._pin.value()

    def check(self):
        new_value = self._pin.value()
        if new_value != self._old_value:
            self._old_value = new_value
            self._counter += self._old_value == 1 # only count rising value

    def get_count(self):
        return self._counter
