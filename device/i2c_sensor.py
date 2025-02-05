from device.sensor import Sensor


class I2cSensor(Sensor):
    def __init__(self, location, device_class, i2c):
        super().__init__(location)
        self._device = device_class(i2c=i2c)

    def reset_channel(self):
        pass

    def ensure_channel(self):
        pass

    def value(self):
        return self._device.value()

    def get_device(self):
        return self._device
