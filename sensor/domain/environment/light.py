# Sensor for the light level (in lux)

class Light:
    def __init__(self, location : str, sensor):
        self.location = location
        self._sensor = sensor

    def light(self):
        return self._sensor.value()
