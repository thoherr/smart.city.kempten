import json

from util.actor import Actor
from report.umqtt.robust import MQTTClient

class DashboardUpload(Actor):
    def __init__(self, actor_id, mqtt_client : MQTTClient, sensor, interval=2, verbose=False):
        super().__init__(actor_id, interval=interval, verbose=verbose)
        self._mqtt_client = mqtt_client
        self._sensor = sensor
        self._current_value = None
        self._value_published = False

    async def work(self):
        new_value = self._sensor.value()
        if new_value != self._current_value or not self._value_published:
            self._current_value = new_value
            self.publish_value()

    def publish_value(self):
        if self._verbose:
            self.log("Uploading dashboard data for sensor %s" % self._sensor)
        topic = self.actor_id
        msg = json.dumps({"self._current_value": self._current_value})
        self._value_published = self._mqtt_client.publish(topic, msg, retain=False, qos=0)
