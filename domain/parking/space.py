# Sensor for a (single) parking space, using a distance sensor
from util.actor import Actor


class ParkingSpace(Actor):
    def __init__(self, parking_space_id, multiplexer, channel, distance_sensor_class, empty_threshold=100, interval=1,
                 verbose=False):
        super().__init__("ParkingSpace {:s}".format(parking_space_id), interval, verbose)
        self._multiplexer = multiplexer
        self._channel = channel
        self._multiplexer.switch_to_channel(self._channel)
        self._distance_sensor = distance_sensor_class(self._multiplexer.i2c)
        self._empty_threshold = empty_threshold
        self._interval = interval
        self._is_empty = True

    async def work(self):
        self._multiplexer.switch_to_channel(self._channel)
        distance = self._distance_sensor.value()
        if self._verbose:
            self.log("distance = {:d}".format(self._channel, distance))
        self._is_empty = (distance > self._empty_threshold)

    def empty(self):
        return self._is_empty
