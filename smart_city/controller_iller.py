# This is the third Raspi of our MOC of the City of Kempten
# It implements the Illerufer (second baseplate), nearby the river, with a Parking Area (including display),
# three waste containers and one traffic light
# Due to memory use this code does not run on a Pico W, use a Pico 2 W instead
import gc

from machine import Pin

from device.driver.BME280 import BME280
from device.driver.gy302 import GY302
from device.driver.tca9548a import TCA9548A
from device.driver.vl53l0x import VL53L0X
from device.i2c_multiplexer import I2cMultiplexer
from device.multiplexed_i2c_sensor import MultiplexedI2cSensor

from setup_values import *

gc.collect()

from domain.environment.light import Light
from domain.environment.weather import Weather
from domain.environment import Environment
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from domain.traffic.count import TrafficCount
from domain.traffic.light.column import Column as TrafficLightColumn
from domain.traffic.light.crossing import Crossing as TrafficLightCrossing
from domain.waste.area import WasteArea
from domain.waste.container import WasteContainer
gc.collect()

from report.mqtt_upload import MqttUploadActor, MqttUpload
gc.collect()

from report.traffic_count_panel import TrafficCountPanel
from report.parking_area_panel_sh1106 import ParkingAreaPanelSH1106
from report.environment_panel import EnvironmentPanel
gc.collect()

from smart_city.controller_base import ControllerBase


class ControllerIller(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_multiplexers()
        self._init_parking()
        self._init_waste()
        self._init_traffic()
        self._init_environment()

        self.parking_panel = ParkingAreaPanelSH1106(self.i2c0, self.parking, self.waste,
                                                    multiplexer=I2cMultiplexer(self.mux74, 2))
        self.actors.append(self.parking_panel)

    def _init_waste(self):
        w1 = WasteContainer("Illerufer 1",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux72, channel=3), interval=SMART_WASTE_CHECK_INTERVAL)
        self.actors.append(w1)
        w2 = WasteContainer("Illerufer 2",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux72, channel=2), interval=SMART_WASTE_CHECK_INTERVAL)
        self.actors.append(w2)
        w3 = WasteContainer("Illerufer 3",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux72, channel=1), interval=SMART_WASTE_CHECK_INTERVAL)
        self.actors.append(w3)
        self.waste = WasteArea("Iller", [w1, w2, w3])

        self.waste_upload = MqttUploadActor("smart_waste/sck_smart_waste_2", self.mqtt_client, self.waste.status, interval=SMART_WASTE_MQTT_INTERVAL)
        self.actors.append(self.waste_upload)

    def _init_parking(self):
        p1 = ParkingSpace("Illerufer 1",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=5),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=110)
        p2 = ParkingSpace("Illerufer 2",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=4),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=50)
        p3 = ParkingSpace("Illerufer 3",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=3),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=68)
        p4 = ParkingSpace("Illerufer 4",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=2),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=55)
        p5 = ParkingSpace("Illerufer 5",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=1),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=50)
        p6 = ParkingSpace("Illerufer 6",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=0),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=60)
        self.parking = ParkingArea("Illerufer", [p1, p2, p3, p4, p5, p6])
        self.actors.append(self.parking)

        self.parking_upload = MqttUploadActor("parkraum/sck_parkraum_2", self.mqtt_client, self.parking.status, interval=PARKRAUM_MQTT_INTERVAL)
        self.actors.append(self.parking_upload)

    def _init_traffic(self):
        l1 = TrafficLightColumn(9, 10, 11, 1)
        l2 = TrafficLightColumn(14, 13, 12, 0)

        self.actors.append(TrafficLightCrossing("Illerufer", [l1, l2]))

        mqtt_traffic_4 = MqttUpload("verkehr/sck_verkehr_4", self.mqtt_client)

        in_traffic_4 = TrafficCount("RH 4 eingehend", "eingehend", Pin(26, Pin.IN), mqtt_traffic_4, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(in_traffic_4)
        out_traffic_4 = TrafficCount("RH 4 ausgehend", "ausgehend", Pin(27, Pin.IN), mqtt_traffic_4, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(out_traffic_4)

        counters_4 = [in_traffic_4, out_traffic_4]
        self.traffic_count_panel = TrafficCountPanel("traffic", self.mux74.i2c, counters_4,
                                                multiplexer=I2cMultiplexer(self.mux74, 0))
        self.actors.append(self.traffic_count_panel)

        mqtt_traffic_5 = MqttUpload("verkehr/sck_verkehr_5", self.mqtt_client)

        traffic_5 = TrafficCount("RH 5", "durchfahrt", Pin(28, Pin.IN), mqtt_traffic_5, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(traffic_5)

    def _init_environment(self):
        self.weather = Weather("weather",
                               MultiplexedI2cSensor(BME280, multiplexer=self.mux74, channel=3), interval=ENVIRONMENT_CHECK_INTERVAL)
        self.actors.append(self.weather)

        self.light = Light("light", MultiplexedI2cSensor(GY302, multiplexer=self.mux74, channel=3), interval=ENVIRONMENT_CHECK_INTERVAL)
        self.actors.append(self.light)

        self.environment_panel = EnvironmentPanel("environment", self.mux74.i2c, self.weather, self.light,
                                                multiplexer=I2cMultiplexer(self.mux74, 1), interval=ENVIRONMENT_CHECK_INTERVAL)
        self.actors.append(self.environment_panel)

        self.environment = Environment(self.weather, self.light)
        self.env_upload = MqttUploadActor("umwelt/sck_umwelt_1", self.mqtt_client, self.environment.status,
                                          interval=ENVIRONMENT_MQTT_INTERVAL)
        self.actors.append(self.env_upload)

    def _init_multiplexers(self):
        # Name includes address for better reference
        self.mux70 = TCA9548A(self.i2c1, address=0x70)
        self.mux72 = TCA9548A(self.i2c1, address=0x72)
        self.mux74 = TCA9548A(self.i2c0, address=0x74)

