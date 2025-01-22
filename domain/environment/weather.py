
class Weather:
    def __init__(self, location : str,  sensor):
        self.location = location
        self._sensor = sensor

# TODO: Delegate the three value functions to our one and only BME280 (or whatever)

    def temperature(self):
        self._sensor.ensure_channel()
        return self._sensor.get_device().temperature

    def pressure(self):
        self._sensor.ensure_channel()
        return self._sensor.get_device().pressure

    def humidity(self):
        self._sensor.ensure_channel()
        return self._sensor.get_device().humidity
