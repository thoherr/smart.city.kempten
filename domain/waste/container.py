# Sensor for a (single) waste container, using a light barrier
from util.actor import Actor


class WasteContainer(Actor):
    def __init__(self, actor_id: str, sensor, threshold=80, interval=1, verbose=False):
        Actor.__init__(self, actor_id, interval=interval, verbose=verbose)
        self._sensor = sensor
        self._threshold = threshold
        self._is_full = False

    async def work(self):
        value = self._sensor.value()
        if self._verbose:
            self.log(f"Waste {self.actor_id}: {value}")
        self._is_full = value < self._threshold

    def full(self):
        return self._is_full
