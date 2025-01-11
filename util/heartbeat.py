from machine import Pin
import asyncio

class Heartbeat:
    def __init__(self, pin = "LED", interval=1000, ratio=0.05):
        self._led = Pin(pin, Pin.OUT)
        self._interval = interval
        self._ratio = ratio
        self._off_time = int(self._interval * (1.0 - self._ratio))
        self._on_time = int(self._interval * self._ratio)

    async def run(self):
        while True:
            self._led.off()
            await asyncio.sleep_ms(self._off_time)
            self._led.on()
            await asyncio.sleep_ms(self._on_time)
