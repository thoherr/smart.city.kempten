import json

import utime

import setup_mqtt_config as mqtt_config
from report.umqtt.robust import MQTTClient
from util.actor import Actor


class MqttUpload(Actor):
    def __init__(self, actor_id, mqtt_client: MQTTClient, value_method, interval=2, verbose=False):
        super().__init__(actor_id, interval=interval, verbose=verbose)
        self._mqtt_client = mqtt_client
        self._topic = f"{mqtt_config.mqtt_topic_root}/{self.actor_id}"
        self._value_method = value_method
        self._current_value = None

    async def work(self):
        if self._verbose:
            self.log(f"Checking data for {self.actor_id} for MQTT upload")
        new_value = self._value_method()
        if new_value != self._current_value:
            self._current_value = new_value
            self.post_data()

    def post_data(self):
        if self._verbose:
            self.log(f"Uploading changed data for {self.actor_id} to MQTT")
        now = utime.gmtime()
        timestamp = f"{now[0]:4d}-{now[1]:02d}-{now[2]:02d}T{now[3]:02d}:{now[4]:02d}:{now[5]:02d}Z"
        msg = json.dumps({"id": self.actor_id,
                          "timestamp": timestamp,
                          "payload": self._current_value})
        self._mqtt_client.publish(self._topic, msg, retain=False, qos=0)
