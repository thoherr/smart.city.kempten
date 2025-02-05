# TCA9548A Multiplexer

class TCA9548A:
    def __init__(self, i2c, address=0x70):
        self.i2c = i2c
        self._address = address

    def switch_to_channel(self, channel: int = -1):
        if 0 <= channel <= 7:
            mask = 0x01 << channel
        else:
            mask = 0x00

        self.i2c.writeto(self._address, mask.to_bytes(1))
