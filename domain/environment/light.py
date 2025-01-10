# Sensor for the light level (in lux)

class Light:
    def __init__(self, location : str, multiplexer, channel, sensor_class):
        self.location = location
        self._multiplexer = multiplexer
        self._channel = channel
        self._multiplexer.switch_to_channel(self._channel)
        self._sensor = sensor_class(self._multiplexer.i2c)

    def light(self):
        self._multiplexer.switch_to_channel(self._channel)
        return self._sensor.value()
