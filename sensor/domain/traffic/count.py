# Sensor for traffic count, using a PIO (e.g. reed or hall sensor)

class TrafficCount:
    def __init__(self, location : str, binary_sensor):
        self._counter : int = 0
        self.location = location
        self._binary_sensor = binary_sensor
        self._old_value = self._binary_sensor.value()

    def check(self):
        new_value = self._binary_sensor.value()
        if new_value != self._old_value:
            self._old_value = new_value
            self._counter += self._old_value == 1 # only count rising value

    def get_count(self):
        return self._counter
