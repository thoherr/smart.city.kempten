# Sensor for a (single) waste container, using a light barrier
from util.actor import Actor


class WasteContainer(Actor):
    def __init__(self, waste_container_id, location: str, multiplexer, channel, sensor_class, threshold=100, interval=1,
                 verbose=False):
        super().__init__("WasteContainer {:s}".format(waste_container_id), interval, verbose)
        self.location = location
        self._multiplexer = multiplexer
        self._channel = channel
        self._multiplexer.switch_to_channel(self._channel)
        self._sensor = sensor_class(self._multiplexer.i2c)
        self._threshold = threshold
        self._interval = interval
        self._is_full = False

    async def work(self):
        self._multiplexer.switch_to_channel(self._channel)
        self._is_full = self._sensor.value() < self._threshold

    def full(self):
        return self._is_full
