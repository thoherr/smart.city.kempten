import asyncio
import gc

from machine import Pin, I2C

import setup_wlan_config as wlan_config
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper
from util.mqtt import connect_mqtt
from util.wlan import initialize_wlan


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
    def __init__(self, debug=False, do_wlan_init=True, do_mqtt_init=True, **_kwargs):
        self.debug = debug
        self.mqtt_client = None

        if do_wlan_init:
            self.init_wlan()
            if do_mqtt_init:
                gc.collect()
                self.init_mqtt()

        self.i2c0 = I2C(0, sda=Pin(0), scl=Pin(1))
        if self.debug:
            print_i2c_info(0, self.i2c0)

        self.i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))
        if self.debug:
            print_i2c_info(1, self.i2c1)

        self.actors = []

        self.actors.append(Heartbeat(verbose=True))
        self.actors.append(Housekeeper(verbose=True))

    def init_mqtt(self):
        self.mqtt_client = connect_mqtt()
        if self.mqtt_client and self.debug:
            print("##### MQTT setup complete")

    def init_wlan(self):
        if self.debug:
            print("##### WLAN and MQTT setup")
        if initialize_wlan(wlan_config.wlan_ssid, wlan_config.wlan_password) and self.debug:
            print("##### WLAN setup complete")

    def print_debug_log(self):
        pass

    async def create_tasks(self):
        if self.debug:
            print("##### create_tasks()")
        tasks = []
        for actor in self.actors:
            tasks.append(asyncio.create_task(actor.run()))
        return tasks

    async def run_forever(self):
        while True:
            if self.debug:
                self.print_debug_log()
            await asyncio.sleep(5)
