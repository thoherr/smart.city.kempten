# Sensor for traffic count, using a PIO (e.g. reed or hall sensor)
import asyncio


class TrafficCount:
    def __init__(self, location : str, binary_sensor, interval=0.25):
        self._counter : int = 0
        self.location = location
        self._binary_sensor = binary_sensor
        self._interval = interval
        self._old_value = self._binary_sensor.value()

    async def run(self):
        while True:
            new_value = self._binary_sensor.value()
            if new_value != self._old_value:
                self._old_value = new_value
                self._counter += self._old_value == 1 # only count rising value
            await asyncio.sleep(self._interval)

    def get_count(self):
        return self._counter
