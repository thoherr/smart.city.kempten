from report.umqtt.simple import MQTTClient
import setup_mqtt_config as mqtt_config

def connect_mqtt():
    try:
        client = MQTTClient(client_id=mqtt_config.mqtt_client_id,
                            server=mqtt_config.mqtt_server,
                            port=mqtt_config.mqtt_port,
                            user=mqtt_config.mqtt_username,
                            password=mqtt_config.mqtt_password,
                            keepalive=7200,
                            ssl=False)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise
