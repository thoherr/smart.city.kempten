from util.actor import Actor


class Noise(Actor):
    def __init__(self, actor_id: str, analog_sensor, interval=interval, verbose=verbose):
        Actor.__init__(self, actor_id)
        self._analog_sensor = analog_sensor
        self._noise = 0

    async def work(self):
        self._noise = self._analog_sensor.noise()

    def noise(self):
        return self._noise
