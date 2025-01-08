import time

from machine import ADC

from display.freesans20 import min_ch


class KY037:
    def __init__(self, adc_id=0):
        self._adc = ADC(adc_id)

    def value(self):
        min_value = 65538
        max_value = 0
        for i in range(1000):
            raw_value = self._adc.read_u16()
            if raw_value > max_value:
                max_value = raw_value
            if raw_value < min_value:
                min_value = raw_value
            time.sleep(0.002)
        volt = round((max_value - min_value) * 5 / 65536, 2)
        return volt

    def noise(self):
        return self.value()
