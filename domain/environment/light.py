# Sensor for the light level (in lux)
from util.multiplexed_sensor import MultiplexedSensor


class Light(MultiplexedSensor):
    def __init__(self, actor_id : str, i2c, sensor_class, multiplexer=None, channel : int=-1, interval=1, verbose=False):
        super().__init__("LightSensor {:s}".format(actor_id), multiplexer, channel, interval, verbose)
        self.ensure_channel()
        self._sensor = sensor_class(i2c)
        self._value = 0

    async def work(self):
        self.ensure_channel()
        self._value = self._sensor.value()

    def light(self):
        return self._value
