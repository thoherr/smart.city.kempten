from device.i2c_sensor import I2cSensor


class MultiplexedI2cSensor(I2cSensor):
    def __init__(self, location : str, device_class, multiplexer, channel : int):
        self._multiplexer = multiplexer
        self._channel = channel
        self.ensure_channel()
        super().__init__(location, device_class, self._multiplexer.i2c)
        self.reset_channel()

    def reset_channel(self):
        self._multiplexer.switch_to_channel(-1)

    def ensure_channel(self):
        self._multiplexer.switch_to_channel(self._channel)

    def value(self):
        self.ensure_channel()
        value = self._device.value()
        self.reset_channel()
        return value
