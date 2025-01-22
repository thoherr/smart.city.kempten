# Sensor for a (single) parking space, using a distance sensor
from util.multiplexed_sensor import MultiplexedSensor


class ParkingSpace(MultiplexedSensor):
    def __init__(self, parking_space_id, i2c, distance_sensor_class, multiplexer=None, channel : int=-1,
                 empty_threshold=100, interval=1, verbose=False):
        super().__init__("ParkingSpace {:s}".format(parking_space_id), multiplexer, channel, interval, verbose)
        self.ensure_channel()
        self._distance_sensor = distance_sensor_class(i2c)
        self._empty_threshold = empty_threshold
        self._interval = interval
        self._is_empty = True

    async def work(self):
        self.ensure_channel()
        distance = self._distance_sensor.value()
        self.reset_channel()
        if self._verbose:
            self.log("distance = {:d}".format(distance))
        self._is_empty = (distance > self._empty_threshold)

    def empty(self):
        return self._is_empty
