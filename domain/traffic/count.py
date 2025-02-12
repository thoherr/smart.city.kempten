# Sensor for traffic count, using a PIO (e.g. reed or hall driver)
import asyncio

from report.mqtt_upload import MqttUpload
from util.actor import Actor


class TrafficCount(Actor):
    def __init__(self, actor_id: str, direction: str, gpio_pin, mqtt_upload: MqttUpload = None, interval=0.05, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._counter: int = 0
        self._direction = direction
        self._gpio_pin = gpio_pin
        self._old_value = self._gpio_pin.value()
        self._mqtt_upload = mqtt_upload

    async def work(self):
        new_value = self._gpio_pin.value()
        if new_value != self._old_value:
            if self._verbose:
                self.log(f"new value: {new_value}")
            if new_value == 1:  # only count rising value
                self._counter += (new_value == 1)
                if self._mqtt_upload:
                    data = {"Richtung": self._direction, "Summe": self._counter}
                    if self._verbose:
                        self.log(f"mqtt_upload {data} begin")
                    self._mqtt_upload.post_data(data)
                    if self._verbose:
                       self.log(f"mqtt_upload {data} end")
            self._old_value = new_value

    def value(self):
        return self._counter
