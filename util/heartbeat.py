import asyncio
import time

from machine import Pin

from util.actor import Actor


class Heartbeat(Actor):
    def __init__(self, actor_id="Heartbeat", pin="LED", interval=1, ratio=0.05, print_timestamp=False):
        super().__init__(actor_id, interval)
        self._led = Pin(pin, Pin.OUT)
        self._ratio = ratio
        self._interval = self._interval * (1.0 - self._ratio)
        self._on_time = self._interval * self._ratio
        self._print_timestamp = print_timestamp
        self._counter = 0

    async def work(self):
        self._led.on()
        self._counter = self._counter + 1
        if self._print_timestamp:
            now = time.gmtime()
            self.log(str(self._counter))
        await asyncio.sleep(self._on_time)
        self._led.off()
