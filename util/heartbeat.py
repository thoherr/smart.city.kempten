import time

from machine import Pin
import asyncio

class Heartbeat:
    def __init__(self, pin = "LED", interval=1000, ratio=0.05, print_timestamp=False):
        self._led = Pin(pin, Pin.OUT)
        self._interval = interval
        self._ratio = ratio
        self._print_timestamp = print_timestamp
        self._off_time = int(self._interval * (1.0 - self._ratio))
        self._on_time = int(self._interval * self._ratio)

    async def run(self):
        while True:
            self._led.off()
            await asyncio.sleep_ms(self._off_time)
            self._led.on()
            if self._print_timestamp:
                now = time.gmtime()
                print("{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} heartbeat".format(now[0], now[1], now[2], now[3], now[4], now[5]))
            await asyncio.sleep_ms(self._on_time)
