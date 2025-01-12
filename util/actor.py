import asyncio
import time


class Actor:
    def __init__(self, actor_id, interval=1, verbose=False):
        self.id = actor_id
        self._interval = interval
        self._verbose = verbose

    async def run(self):
        while True:
            await self.work()
            await asyncio.sleep(self._interval)

    async def work(self):
        if self._verbose:
            print("base class work() called from actor {}".format(self.id))

    def log(self, content):
        now = time.gmtime()
        print("{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} - {:s} - {:s}".format(now[0], now[1], now[2], now[3], now[4],
                                                                        now[5], self.id, content))
