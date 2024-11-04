
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23

class GY302:
    def __init__(self, i2c, instance=0):
        self.i2c = i2c
        self.address = 0x23 if instance == 0 else 0x5C

    @staticmethod
    def convert_to_number(data):
        result=(data[1] + (256 * data[0])) / 1.2
        return result

    def value(self):
        data = self.i2c.readfrom_mem(self.address, ONE_TIME_HIGH_RES_MODE_1, 3)
        return self.convert_to_number(data)
