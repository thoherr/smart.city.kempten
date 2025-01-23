# Sensor for a (single) parking space, using a distance driver
from device.multiplexed_i2c_sensor import MultiplexedI2cSensor
from util.actor import Actor


class ParkingSpace(Actor):
    def __init__(self, parking_space_id, sensor, empty_threshold=100, interval=1, verbose=False):
        super().__init__(parking_space_id, interval=interval, verbose=verbose)
        self._sensor = sensor
        self._empty_threshold = empty_threshold
        self._is_empty = True

    async def work(self):
        distance = self._sensor.value()
        if self._verbose:
            self.log("distance = {:d}".format(distance))
        self._is_empty = (distance > self._empty_threshold)

    def empty(self):
        return self._is_empty
