# Sensor for traffic count, using a PIO (e.g. reed or hall driver)

from util.actor import Actor


class TrafficCount(Actor):
    def __init__(self, location: str, binary_sensor, interval=0.2, verbose=False):
        super().__init__(location, interval, verbose)
        self._counter: int = 0
        self._binary_sensor = binary_sensor
        self._old_value = self._binary_sensor.value()

    async def work(self):
        new_value = self._binary_sensor.value()
        if new_value != self._old_value:
            self._counter += (new_value == 1)  # only count rising value
            self._old_value = new_value

    def value(self):
        return self._counter
