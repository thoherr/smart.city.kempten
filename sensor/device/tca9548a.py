# TCA9548A Multiplexer

class TCA9548A:
    def __init__(self, i2c, address=0x70):
        self._i2c = i2c
        self._address = address

    def switch_to_channel(self, channel : int = -1):
        mask = b'0x00'
        # TODO/FIXME: This could be done way mor efficient with a shift
        if channel == 0:
            mask = b'0x01'
        elif channel == 1:
            mask = b'0x02'
        elif channel == 2:
            mask = b'0x04'
        elif channel == 3:
            mask = b'0x08'
        elif channel == 4:
            mask = b'0x10'
        elif channel == 5:
            mask = b'0x20'
        elif channel == 6:
            mask = b'0x40'
        elif channel == 7:
            mask = b'0x80'
        else:
            mask = b'0x00'

        self._i2c.writeto(self._address, mask)
