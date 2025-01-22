import asyncio
import time


class Actor:
    def __init__(self, actor_id, interval=1, verbose=False, debug=False):
        self.actor_id = actor_id
        self._interval = interval
        self._verbose = verbose
        self._debug = debug
        if self._verbose:
            self.log('actor id {} initialized'.format(self.actor_id))

    async def run(self):
        while True:
            if self._debug:
                self.log('actor id: {} calling work()'.format(self.actor_id))
            await self.work()
            await asyncio.sleep(self._interval)

    async def work(self):
        if self._verbose:
            self.log("base class work() called from actor {}".format(self.actor_id))

    def log(self, content):
        now = time.gmtime()
        print("{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} - {:s} - {:s}".format(now[0], now[1], now[2], now[3], now[4],
                                                                              now[5], self.actor_id, content))
