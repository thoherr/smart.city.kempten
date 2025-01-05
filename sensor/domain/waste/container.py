# Sensor for a (single) waste container, using a light barrier

class WasteContainer:
    def __init__(self, location, multiplexer, channel, sensor_class, threshold=100):
        self.location = location
        self._multiplexer = multiplexer
        self._channel = channel
        self._multiplexer.switch_to_channel(self._channel)
        self._sensor = sensor_class(self._multiplexer.i2c)
        self._threshold = threshold
        self._is_full = False

    def check(self):
        self._multiplexer.switch_to_channel(self._channel)
        self._is_full = self._sensor.value() < self._threshold

    def full(self):
        return self._is_full
