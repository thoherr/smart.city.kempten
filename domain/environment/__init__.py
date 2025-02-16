from domain.environment.light import Light
from domain.environment.weather import Weather

class Environment:
    def __init__(self, w: Weather, l: Light):
        self._weather = w
        self._light = l

    def status(self):
        return self._weather.status() | self._light.status()
