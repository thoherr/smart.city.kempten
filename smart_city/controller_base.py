from machine import Pin, I2C


class ControllerBase(object):
    def __init__(self, **_kwargs):
        self.i2c0 = I2C(0, sda=Pin(0), scl=Pin(1))
        self.i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))

    def print_i2c_debug_info(self):
        print('Scan I2C Bus 0...')
        i2c_devices = self.i2c0.scan()
        if len(i2c_devices) == 0:
            print('Kein I2C-Gerät an I2C 0 gefunden!')
        else:
            print('I2C-Geräte gefunden:', len(i2c_devices))
            for i2c_dev in i2c_devices:
                print('Dezimale Adresse:', i2c_dev, '| Hexadezimale Adresse:', hex(i2c_dev))

        print('Scan I2C Bus 1...')
        i2c_devices = self.i2c1.scan()
        if len(i2c_devices) == 0:
            print('Kein I2C-Gerät an I2C 1 gefunden!')
        else:
            print('I2C-Geräte gefunden:', len(i2c_devices))
            for i2c_dev in i2c_devices:
                print('Dezimale Adresse:', i2c_dev, '| Hexadezimale Adresse:', hex(i2c_dev))

