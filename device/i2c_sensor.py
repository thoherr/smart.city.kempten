
class I2cSensor:
    def __init__(self, device_class, i2c):
        self._device = device_class(i2c=i2c)

    def reset_channel(self):
        pass

    def ensure_channel(self):
        pass

    def value(self):
        return self._device.value()

    def get_device(self):
        return self._device