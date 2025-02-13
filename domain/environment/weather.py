from util.actor import Actor


class Weather(Actor):
    def __init__(self, actor_id, sensor, interval=10, verbose=False):
        super().__init__(actor_id, interval=interval, verbose=verbose)
        self._sensor = sensor
        self._temperature = 0
        self._pressure = 0
        self._humidity = 0

    async def work(self):
        # TODO: Despite our default structure, the BME280 driver has three property methods instead of a value method
        self._sensor.ensure_channel()
        self._temperature = self._sensor.get_device().temperature
        self._pressure = self._sensor.get_device().pressure
        self._humidity = self._sensor.get_device().humidity
        self._sensor.reset_channel()

    def temperature(self):
        return self._temperature

    def pressure(self):
        return self._pressure

    def humidity(self):
        return self._humidity

    def status(self):
        return { "Temperatur": self._temperature,
                 "Luftdruck": self._pressure,
                 "Luftfeuchte": self._humidity }
