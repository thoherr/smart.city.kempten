from util.actor import Actor


class MultiplexedActor(Actor):
    def __init__(self, actor_id, multiplexer=None, channel : int=-1, interval=1, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._multiplexer = multiplexer
        self._channel = channel

    def ensure_channel(self):
        if self._multiplexer is not None:
            self._multiplexer.switch_to_channel(self._channel)

