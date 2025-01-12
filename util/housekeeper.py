import asyncio
import gc

from util import memory_usage
from util.actor import Actor


class Housekeeper(Actor):
    def __init__(self, interval=1, verbose=False):
        super().__init__("Housekeeper", interval, verbose)
        self._interval = interval
        self._verbose = verbose

    async def work(self):
        if self._verbose:
            self.log(memory_usage.free(True))
        gc.collect()
        if self._verbose:
            self.log(memory_usage.free(True))
