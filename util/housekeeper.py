import asyncio
import gc

from util import memory_usage


class Housekeeper:
    def __init__(self, interval=1, verbose=False):
        self._interval = interval
        self._verbose = verbose

    async def run(self):
        while True:
            if self._verbose:
                print(memory_usage.free(True))
            gc.collect()
            if self._verbose:
                print(memory_usage.free(True))
            await asyncio.sleep(self._interval)
