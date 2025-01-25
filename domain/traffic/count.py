# Sensor for traffic count, using a PIO (e.g. reed or hall driver)

from util.actor import Actor


class TrafficCount(Actor):
    def __init__(self, actor_id: str, gpio_pin, interval=0.2, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._counter: int = 0
        self._gpio_pin = gpio_pin
        self._old_value = self._gpio_pin.value()

    async def work(self):
        new_value = self._gpio_pin.value()
        if new_value != self._old_value:
            self._counter += (new_value == 1)  # only count rising value
            self._old_value = new_value

    def value(self):
        return self._counter
