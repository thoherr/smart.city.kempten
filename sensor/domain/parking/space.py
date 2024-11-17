# Sensor for a (single) parking space, using a distance sensor

class ParkingSpace:
    def __init__(self, multiplexer, channel, distance_sensor, empty_threshold):
        self._multiplexer = multiplexer
        self._channel = channel
        self._distance_sensor = distance_sensor
        self._empty_threshold = empty_threshold
        self._is_empty = True

    def check(self):
        self._multiplexer.switch_to_channel(self._channel)
        self._is_empty = self._distance_sensor.value() > self._empty_threshold

    def empty(self):
        return self._is_empty
