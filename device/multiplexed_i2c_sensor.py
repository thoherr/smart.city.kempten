from device.i2c_multiplexer import I2cMultiplexer
from device.i2c_sensor import I2cSensor


class MultiplexedI2cSensor(I2cMultiplexer, I2cSensor):
    def __init__(self, device_class, multiplexer, channel : int):
        I2cMultiplexer.__init__(self, multiplexer, channel)
        self.ensure_channel()
        I2cSensor.__init__(self, device_class, self._multiplexer.i2c)
        self.reset_channel()

    def value(self):
        self.ensure_channel()
        value = self._device.value()
        self.reset_channel()
        return value
