import asyncio
import gc


class Housekeeper:
    def __init__(self, interval=1):
        self._interval = interval

    async def run(self):
        while True:
            gc.collect()
            await asyncio.sleep(self._interval)
