import asyncio
import utime


class Actor:
    def __init__(self, actor_id, interval=1, verbose=False, debug=False):
        self.actor_id = actor_id
        self._interval = interval
        self._verbose = verbose
        self._debug = debug
        if self._verbose:
            self.log(f"actor id {self.actor_id} initialized")

    async def run(self):
        while True:
            if self._debug:
                self.log(f"actor id: {self.actor_id} calling work()")
            await self.work()
            await asyncio.sleep(self._interval)

    async def work(self):
        if self._verbose:
            self.log(f"base class work() called from actor {self.actor_id}")

    def log(self, content):
        now = utime.gmtime()
        print(f"{now[0]:4d}-{now[1]:02d}-{now[2]:02d} {now[3]:02d}:{now[4]:02d}:{now[5]:02d} -"
              f" {self.actor_id:s} - {content:s}")
