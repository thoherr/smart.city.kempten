
class Weather:
    def __init__(self, location, sensor):
        self.location = location
        self._sensor = sensor

    def temperature(self):
        return self._sensor.temperature

    def pressure(self):
        return self._sensor.pressure

    def humidity(self):
        return self._sensor.humidity
