from setup_mqtt_config import config
from util.mqtt_as import MQTTClient


async def connect_mqtt():
    try:
        client = MQTTClient(config)
        await client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise
