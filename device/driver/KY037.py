import asyncio

from machine import ADC


# HINT: The driver has to be calibrated, so that the left LED is OFF in silence and
#       begins to flicker at some noise. In order to pick up the noise, measurement
#       runs in background at a time slice of about one second. Otherwise, the
#       value is more or less random. The value range is quite small, e.g.
#       between 48000 and 52000
class KY037:
    def __init__(self, adc_id=0):
        self._adc = ADC(adc_id)
        self._current_min_value = 0
        self._current_max_value = 0

    async def read(self):
        while True:
            min_value = 65538
            max_value = 0
            for i in range(100):
                raw_value = self._adc.read_u16()
                if raw_value > max_value:
                    max_value = raw_value
                if raw_value < min_value:
                    min_value = raw_value
                await asyncio.sleep_ms(10)
            self._current_min_value = min_value
            self._current_max_value = max_value

    def noise(self):
        return [self._current_min_value, self._current_max_value]
