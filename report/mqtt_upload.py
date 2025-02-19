import asyncio
import json

import utime

import setup_mqtt_config as mqtt_config
from util.mqtt_as import MQTTClient
from util.actor import Actor

class MqttUpload:

    def __init__(self, mqtt_topic, mqtt_client: MQTTClient, qos: int = 0, verbose=False):
        self._mqtt_topic = mqtt_topic
        self._verbose = verbose
        self._topic = f"{mqtt_config.mqtt_topic_root}/{self._mqtt_topic}"
        self._mqtt_client = mqtt_client
        self._qos = qos

    def post_data(self, data):
        now = utime.gmtime()
        timestamp = f"{now[0]:4d}-{now[1]:02d}-{now[2]:02d}T{now[3]:02d}:{now[4]:02d}:{now[5]:02d}Z"
        msg = json.dumps({"id": self._mqtt_topic,
                          "timestamp": timestamp,
                          "payload": data})
        asyncio.create_task(self._mqtt_client.publish(self._topic, msg, retain=False, qos=self._qos))
        asyncio.sleep(0)


class MqttUploadActor(MqttUpload, Actor):
    def __init__(self, mqtt_topic, mqtt_client: MQTTClient, value_method, interval=2, verbose=False):
        MqttUpload.__init__(self, mqtt_topic, mqtt_client, verbose=False)
        Actor.__init__(self, mqtt_topic, interval=interval, verbose=verbose)
        self._value_method = value_method
        self._current_value = None

    async def work(self):
        if self._verbose:
            self.log(f"Checking data for {self.actor_id} for MQTT upload")
        new_value = self._value_method()
        if new_value != self._current_value:
            self._current_value = new_value
            if self._verbose:
                self.log(f"Uploading changed data for {self.actor_id} to MQTT")
            self.post_data(new_value)
