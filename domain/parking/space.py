# Sensor for a (single) parking space, using a distance driver
from util.actor import Actor


class ParkingSpace(Actor):
    def __init__(self, actor_id, sensor, empty_threshold=100, **kwargs):
        super(ParkingSpace, self).__init__(actor_id, **kwargs)
        self._sensor = sensor
        self._empty_threshold = empty_threshold
        self._is_empty = True
        self._distance_average = None
        self._counter = 0

    async def work(self):
        distance = self._sensor.value()
        if self._verbose:
            self._distance_average = ((0 if self._distance_average is None else self._distance_average) *
                                      self._counter + distance) / (self._counter + 1)
            self.log("distance = {:d}, average = {:.2f}".format(distance, self._distance_average))
        self._counter += 1
        self._is_empty = (distance > self._empty_threshold)
        if self._verbose:
            self.log("{:s}".format("empty" if self._is_empty else "occupied"))

    def empty(self):
        return self._is_empty
