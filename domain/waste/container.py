# Sensor for a (single) waste container, using a light barrier
from util.multiplexed_actor import MultiplexedActor


class WasteContainer(MultiplexedActor):
    def __init__(self, location: str, i2c, sensor_class, multiplexer=None, channel : int=-1, threshold=100,
                 interval=1, verbose=False):
        super().__init__(location, multiplexer, channel, interval, verbose)
        self._sensor = sensor_class(i2c)
        self._threshold = threshold
        self._is_full = False

    async def work(self):
        self.ensure_channel()
        value = self._sensor.value()
        if self._verbose:
            self.log(f"Waste {self.id}: {value}")
        self._is_full = value < self._threshold

    def full(self):
        return self._is_full
