import asyncio

import gc
import micropython

from device.i2c_sensor import I2cSensor
from device.multiplexed_i2c_sensor import MultiplexedI2cSensor
from domain.environment.light import Light
from domain.environment.noise import Noise
from domain.environment.weather import Weather
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from domain.traffic.count import TrafficCount
from domain.waste.area import WasteArea
from domain.waste.container import WasteContainer
from report.mqtt_upload import MqttUpload
from report.parking_area_panel import ParkingAreaPanelSH1106
from report.traffic_count_panel import TrafficCountPanel
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper
from util.mqtt import connect_mqtt
from util.wlan import initialize_wlan

micropython.alloc_emergency_exception_buf(100)

from machine import Pin, I2C

from device.driver.tca9548a import TCA9548A
from device.driver.vl53l0x import VL53L0X
from device.driver.gy302 import GY302
from device.driver.BME280 import BME280
from device.driver.KY037 import KY037

import setup_wlan_config as wlan_config
import setup_mqtt_config as mqtt_config

print("##### WLAN and MQTT setup")
if initialize_wlan(wlan_config.wlan_ssid, wlan_config.wlan_password):
    print("##### WLAN setup complete")
gc.enable()
mqtt_client = connect_mqtt()
if mqtt_client:
    print("##### MQTT setup complete")

i2c0 = I2C(0, sda=Pin(0), scl=Pin(1))
i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))

print('Scan I2C Bus 0...')
i2c_devices = i2c0.scan()
if len(i2c_devices) == 0:
    print('Kein I2C-Gerät an I2C 0 gefunden!')
else:
    print('I2C-Geräte gefunden:', len(i2c_devices))
    for i2c_dev in i2c_devices:
        print('Dezimale Adresse:', i2c_dev, '| Hexadezimale Adresse:', hex(i2c_dev))

print('Scan I2C Bus 1...')
i2c_devices = i2c1.scan()
if len(i2c_devices) == 0:
    print('Kein I2C-Gerät an I2C 1 gefunden!')
else:
    print('I2C-Geräte gefunden:', len(i2c_devices))
    for i2c_dev in i2c_devices:
        print('Dezimale Adresse:', i2c_dev, '| Hexadezimale Adresse:', hex(i2c_dev))

multiplexer = TCA9548A(i2c1)
p0 = ParkingSpace("P0", MultiplexedI2cSensor("P0", VL53L0X, multiplexer, 0))
p4 = ParkingSpace("P4", MultiplexedI2cSensor("P4", VL53L0X, multiplexer, 4))
parking = ParkingArea("Rathaus", [p0, p4, p0, p4, p0, p4, p0, p4, p0, p4, p0])

waste_sensor = I2cSensor("Müll", GY302, i2c1)
waste_container_1 = WasteContainer("Müll 1", waste_sensor)
waste_container_2 = WasteContainer("Müll 2", waste_sensor)
waste_container_3 = WasteContainer("Müll 3", waste_sensor)
waste = WasteArea("Müll", [waste_container_1, waste_container_2, waste_container_3])
light_sensor = Light("Fußgängerzone", I2cSensor("Light 1", GY302, i2c1))
weather_sensor = Weather("Innenstadt",
                         MultiplexedI2cSensor("Weather", BME280, multiplexer=multiplexer, channel=7), interval=5)
ky037 = KY037()
noise_sensor = Noise("Strassenlärm", ky037)

traffic_pin = Pin(14, Pin.IN)
traffic = TrafficCount("Rathausplatz", traffic_pin)

traffic_count_panel = TrafficCountPanel("traffic", i2c1, [traffic, traffic], verbose=True)
parking_panel_large = ParkingAreaPanelSH1106(i2c0, parking, waste, verbose=True)

traffic_count_upload = MqttUpload("traffic/cityhall", mqtt_client, traffic.value)
temperature_upload = MqttUpload("weather/temperature", mqtt_client, weather_sensor.temperature, interval=5)
pressure_upload = MqttUpload("weather/pressure", mqtt_client, weather_sensor.pressure, interval=5)
humidity_upload = MqttUpload("weather/humidity", mqtt_client, weather_sensor.humidity, interval=5)
waste_upload = MqttUpload("smart_waste/sck_smart_waste_1", mqtt_client, waste.status, interval=5)


async def main_loop():
    print("----- main_loop starting")
    while True:
        #        waste_status = "{:s} {:s}, {:s} {:s}, {:s} {:s}".format(waste_container_1.actor_id,
        #                                                                "full" if waste_container_1.full() else "OK",
        #                                                                waste_container_2.actor_id,
        #                                                                "full" if waste_container_2.full() else "OK",
        #                                                                waste_container_3.actor_id,
        #                                                                "full" if waste_container_3.full() else "OK")
        waste_status = f"{waste.status()}"
        multiplexer.switch_to_channel(0)
        traffic_count = "Traffic at {:s} {:1d}".format(traffic.actor_id, traffic.value())
        number_of_empty_spaces = parking.number_of_empty_spaces()
        number_of_spaces = parking.number_of_spaces()
        parking_lots = "{:1d} / {:1d}".format(number_of_empty_spaces, number_of_spaces)

        weather = "Weather at {:s}:\n  Temperature {:.2f} °C\n  Pressure {:.2f} hPa\n  Humidity {:.2f} %".format(
            weather_sensor.actor_id, weather_sensor.temperature(), weather_sensor.pressure(), weather_sensor.humidity())
        light = "Light at {:s} is {:.2f}".format(light_sensor.actor_id, light_sensor.light())
        noise = "Noise at {:s} is {}".format(noise_sensor.location, noise_sensor.noise())

        print(waste_status)
        print(traffic_count)
        print(parking_lots)
        print(weather)
        print(light)
        print(noise)

        await asyncio.sleep(0.5)


async def main():
    print("##### main starting")
    await asyncio.gather(asyncio.create_task(ky037.read()),
                         asyncio.create_task(main_loop()),
                         asyncio.create_task(traffic.run()),
                         asyncio.create_task(parking.run()),
                         asyncio.create_task(waste.run()),
                         asyncio.create_task(light_sensor.run()),
                         asyncio.create_task(parking_panel_large.run()),
                         asyncio.create_task(traffic_count_panel.run()),
                         asyncio.create_task(traffic_count_upload.run()),
                         asyncio.create_task(weather_sensor.run()),
                         asyncio.create_task(temperature_upload.run()),
                         asyncio.create_task(humidity_upload.run()),
                         asyncio.create_task(pressure_upload.run()),
                         asyncio.create_task(waste_upload.run()),
                         asyncio.create_task(Heartbeat(verbose=True).run()),
                         asyncio.create_task(Housekeeper(verbose=True).run()))


print("##### Testboard starting")
asyncio.run(main())
print("##### Testboard done")
