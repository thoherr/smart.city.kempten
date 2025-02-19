from util.mqtt_as import config

config["response_time"] = 10
config["queue_len"] = 5

mqtt_topic_root = 'MQTT_TOPIC_ROOT'

config["ssid"] = "WIFI_SSID"
config["wifi_pw"] = "WIFI_PASSWORD"
config["server"] = "MQTT_BROKER_URL"
config["ssl"] = False
config["user"] = "BROKER_USERNAME"
config["password"] = "BROKER_PASSWORD"
