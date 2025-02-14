import gc

from util import memory_usage
from util.actor import Actor


class Housekeeper(Actor):
    def __init__(self, actor_id="Housekeeper", interval=1, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._interval = interval
        self._verbose = verbose

    async def work(self):
        if self._verbose:
            self.log(memory_usage.free(True))
        gc.collect()
        if self._verbose:
            self.log(memory_usage.free(True))

    def status(self):
        mem_free, mem_alloc, mem_total, percentage_free = memory_usage.memory()
        return { "free": mem_free, "alloc": mem_alloc, "total": mem_total, "percentage": percentage_free,
                 "flash": memory_usage.flash() }
