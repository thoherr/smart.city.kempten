
class Weather:
    def __init__(self, location : str,  multiplexer, channel, sensor_class):
        self.location = location
        self._multiplexer = multiplexer
        self._channel = channel
        self._multiplexer.switch_to_channel(self._channel)
        self._sensor = sensor_class(i2c=self._multiplexer.i2c)

    def temperature(self):
        self._multiplexer.switch_to_channel(self._channel)
        return self._sensor.temperature

    def pressure(self):
        self._multiplexer.switch_to_channel(self._channel)
        return self._sensor.pressure

    def humidity(self):
        self._multiplexer.switch_to_channel(self._channel)
        return self._sensor.humidity
