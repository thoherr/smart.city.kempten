from device.i2c_multiplexer import I2cMultiplexer
from device.i2c_sensor import I2cSensor


class MultiplexedI2cSensor(I2cMultiplexer, I2cSensor):
    def __init__(self, device_class, multiplexer, channel : int):
        I2cMultiplexer.__init__(self, multiplexer, channel)
        I2cMultiplexer.ensure_channel(self)
        I2cSensor.__init__(self, device_class, self._multiplexer.i2c)
        I2cMultiplexer.reset_channel(self)

    def value(self):
        I2cMultiplexer.ensure_channel(self)
        value = self._device.value()
        I2cMultiplexer.reset_channel(self)
        return value
