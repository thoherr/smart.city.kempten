# Sensor for a (single) parking space, using a distance sensor
import asyncio


class ParkingSpace:
    def __init__(self, multiplexer, channel, distance_sensor_class, empty_threshold=100, interval=1):
        self._multiplexer = multiplexer
        self._channel = channel
        self._multiplexer.switch_to_channel(self._channel)
        self._distance_sensor = distance_sensor_class(self._multiplexer.i2c)
        self._empty_threshold = empty_threshold
        self._interval = interval
        self._is_empty = True

    async def run(self):
        while True:
            self._multiplexer.switch_to_channel(self._channel)
            distance = self._distance_sensor.value()
            print("Sensor {:d} has value {:d}".format(self._channel, distance))
            self._is_empty = (distance > self._empty_threshold)
            await asyncio.sleep(self._interval)

    def empty(self):
        return self._is_empty
