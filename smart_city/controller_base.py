import asyncio

from machine import Pin, I2C

import setup_values
from report.mqtt_upload import MqttUploadActor
from setup_mqtt_config import config
from util.mqtt_as import MQTTClient

from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper
from util.ntp_time_actor import NtpTimeActor


def print_i2c_info(i2c_id, i2c):
    print(f"##### Scan I2C Bus {i2c_id}...")
    i2c_devices = i2c.scan()

    if len(i2c_devices) == 0:
        print(f"##### No I2C devices at port {i2c_id}")
    else:
        print(f'##### {len(i2c_devices)} I2C devices at port {i2c_id}:', )
        for i2c_dev in i2c_devices:
            print('#####    Decimal address ', i2c_dev, ', HEX address ', hex(i2c_dev))


class ControllerBase(object):
    def __init__(self, number=None, debug=False, **_kwargs):
        self.number = number
        self.debug = debug
        MQTTClient.DEBUG = self.debug
        self.mqtt_client = MQTTClient(config)

        self.i2c0 = I2C(0, sda=Pin(0), scl=Pin(1))
        if self.debug:
            print_i2c_info(0, self.i2c0)

        self.i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))
        if self.debug:
            print_i2c_info(1, self.i2c1)

        self.actors = []

        self.actors.append(Heartbeat())
        self.housekeeper = Housekeeper()
        self.actors.append(self.housekeeper)
        health_upload = MqttUploadActor(f"health_check/sck_health_check_{self.number}", self.mqtt_client,
                                        self.housekeeper.status, interval=setup_values.HEALTH_CHECK_MQTT_INTERVAL)
        self.actors.append(health_upload)
        self.ntp_time = NtpTimeActor(interval=setup_values.NTP_QUERY_INTERVAL, verbose=setup_values.NTP_TIME_VERBOSITY)
        self.actors.append(self.ntp_time)

    def print_debug_log(self):
        pass

    async def up(self):
        while True:
            if self.debug:
                print("##### ControllerBase waits for MQTT broker up()")
            await self.mqtt_client.up.wait()
            self.mqtt_client.up.clear()
            if self.debug:
                print("##### ControllerBase calls settime()")
            self.ntp_time.set_time()
            if self.debug:
                print("##### ControllerBase called settime()")
            if self.debug:
                print("##### MQTT broker up()")

    async def create_tasks(self):
        if self.debug:
            print("##### create_tasks()")
        tasks = [asyncio.create_task(self.up())]
        for actor in self.actors:
            tasks.append(asyncio.create_task(actor.run()))
        return tasks

    async def run_forever(self):
        if self.debug:
            print("##### ControllerBase.run_forever()")
        try:
            await self.mqtt_client.connect()
        except Exception as e:
            print('Error connecting to MQTT:', e)
            raise
        if self.debug:
            print("##### MQTT setup complete")

        while True:
            if self.debug:
                self.print_debug_log()
            await asyncio.sleep(5)
