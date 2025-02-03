import json

from util.actor import Actor
from report.umqtt.robust import MQTTClient

class DashboardUpload(Actor):
    def __init__(self, actor_id, mqtt_client : MQTTClient, topic, value_method, interval=2, verbose=False):
        super().__init__(actor_id, interval=interval, verbose=verbose)
        self._mqtt_client = mqtt_client
        self._topic = topic
        self._value_method = value_method
        self._current_value = None

    async def work(self):
        self.log(f"Updating dashboard for {self.actor_id}")
        new_value = self._value_method()
        if new_value != self._current_value:
            self._current_value = new_value
            self.publish_value()

    def publish_value(self):
        if self._verbose:
            self.log(f"Uploading dashboard data for sensor {self.actor_id}")
        msg = json.dumps({"value": self._current_value})
        self._mqtt_client.publish(self._topic, msg, retain=False, qos=0)
