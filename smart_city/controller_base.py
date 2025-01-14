import asyncio

from machine import Pin, I2C


class ControllerBase(object):
    def __init__(self, debug=False, **_kwargs):
        self.debug = debug
        self.i2c0 = I2C(0, sda=Pin(0), scl=Pin(1))
        self.i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))
        if self.debug:
            self.print_i2c_info()

    def print_debug_log(self):
        pass


    def print_i2c_info(self):
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

    async def run_forever(self):
        while True:
            if self.debug:
                self.print_debug_log()
            await asyncio.sleep(5)
