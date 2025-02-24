import gc

from util import memory_usage, cpu_temperature
from util.actor import Actor


class Housekeeper(Actor):
    def __init__(self, actor_id="Housekeeper", interval=1, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._interval = interval
        self._verbose = verbose
        gc.enable()
        self.mem_free, self.mem_alloc, self.mem_total, self.percentage_free = memory_usage.memory()

    async def work(self):
        if self._verbose:
            self.log(memory_usage.free(True))
        gc.collect()
        self.mem_free, self.mem_alloc, self.mem_total, self.percentage_free = memory_usage.memory()
        if self._verbose:
            self.log(memory_usage.free(True))

    def status(self):
        flash = memory_usage.flash()
        temperature = cpu_temperature.value()
        if self._verbose:
            self.log(f"mem_free={self.mem_free}, mem_alloc={self.mem_alloc}, mem_total={self.mem_total}, percentage_free={self.percentage_free}, flash={flash}")
        return { "free": self.mem_free, "alloc": self.mem_alloc, "total": self.mem_total, "percentage": self.percentage_free,
                 "flash": flash,
                 "temperature": temperature }
