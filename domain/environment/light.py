# Sensor for the light level (in lux)
from util.actor import Actor


class Light(Actor):
    def __init__(self, actor_id: str, sensor, interval=1, verbose=False):
        Actor.__init__(self, actor_id, interval=interval, verbose=verbose)
        self._sensor = sensor
        self._light = 0

    async def work(self):
        self._light = self._sensor.value()

    def light(self):
        return self._light

    def status(self):
        return { "helligkeit": self._light }
