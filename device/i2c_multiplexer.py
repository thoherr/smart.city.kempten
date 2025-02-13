
class I2cMultiplexer:
    def __init__(self, multiplexer, channel : int):
        self._multiplexer = multiplexer
        self._channel = channel
        self.ensure_channel()

    def reset_channel(self):
        self._multiplexer.switch_to_channel(-1)

    def ensure_channel(self):
        self._multiplexer.switch_to_channel(self._channel)
