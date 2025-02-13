# This is the third Raspi of our MOC of the City of Kempten
# It implements the Illerufer (second baseplate), nearby the river, with a Parking Area (including display),
# three waste containers and one traffic light
import gc

from machine import Pin

from device.driver.BME280 import BME280
from device.driver.gy302 import GY302
from device.driver.tca9548a import TCA9548A
from device.driver.vl53l0x import VL53L0X
from device.i2c_multiplexer import I2cMultiplexer
from device.multiplexed_i2c_sensor import MultiplexedI2cSensor
gc.collect()

from domain.environment.light import Light
from domain.environment.weather import Weather
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from domain.traffic.count import TrafficCount
from domain.waste.area import WasteArea
from domain.waste.container import WasteContainer
from report.mqtt_upload import MqttUploadActor, MqttUpload
gc.collect()

from report.traffic_count_panel import TrafficCountPanel
#from report.parking_area_panel_sh1106 import ParkingAreaPanelSH1106
gc.collect()

from smart_city.controller_base import ControllerBase


class ControllerIller(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_multiplexers()
        gc.collect()
        self._init_parking()
        gc.collect()
        self._init_waste()
        gc.collect()
        self._init_traffic()
        gc.collect()
        self._init_environment()

#        self.parking_panel_large = ParkingAreaPanelSH1106(self.i2c0, self.parking, self.waste, verbose=False)
#        self.actors.append(self.parking_panel_large)

    def _init_waste(self):
        w1 = WasteContainer("Illerufer 1",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux72, channel=3),
                            verbose=True)
        self.actors.append(w1)
        w2 = WasteContainer("Illerufer 2",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux72, channel=2),
                            verbose=True)
        self.actors.append(w2)
        w3 = WasteContainer("Illerufer 3",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux72, channel=1),
                            verbose=True)
        self.actors.append(w3)
        self.waste = WasteArea("Iller", [w1, w2, w3])

        self.waste_upload = MqttUploadActor("smart_waste/sck_smart_waste_2", self.mqtt_client, self.waste.status, interval=3,
                                            verbose=True)
        self.actors.append(self.waste_upload)

    def _init_parking(self):
        p1 = ParkingSpace("Illerufer 1",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=5),
                          empty_threshold=110, verbose=True)
        p2 = ParkingSpace("Illerufer 2",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=4),
                          empty_threshold=50, verbose=True)
        p3 = ParkingSpace("Illerufer 3",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=3),
                          empty_threshold=68, verbose=True)
        p4 = ParkingSpace("Illerufer 4",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=2),
                          empty_threshold=55, verbose=True)
        p5 = ParkingSpace("Illerufer 5",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=1),
                          empty_threshold=50, verbose=True)
        p6 = ParkingSpace("Illerufer 6",
                          MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux70, channel=0),
                          empty_threshold=60, verbose=True)
        self.parking = ParkingArea("Illerufer", [p1, p2, p3, p4, p5, p6])
        self.actors.append(self.parking)

        self.parking_upload = MqttUploadActor("parkraum/sck_parkraum_2", self.mqtt_client, self.parking.status, interval=3,
                                              verbose=True)
        self.actors.append(self.parking_upload)

    def _init_traffic(self):
        mqtt_traffic_4 = MqttUpload("verkehr/sck_verkehr_4", self.mqtt_client, verbose=True)

        in_traffic_4 = TrafficCount("RH 4 einwärts", "eingehend", Pin(26, Pin.IN), mqtt_traffic_4, verbose=True)
        self.actors.append(in_traffic_4)
        out_traffic_4 = TrafficCount("RH 4 auswärts", "ausgehend", Pin(27, Pin.IN), mqtt_traffic_4, verbose=True)
        self.actors.append(out_traffic_4)

        counters_4 = [in_traffic_4, out_traffic_4]
        traffic_count_panel = TrafficCountPanel("traffic", self.mux74.i2c, counters_4,
                                                multiplexer=I2cMultiplexer(self.mux74, 0), verbose=True)
        self.actors.append(traffic_count_panel)

        mqtt_traffic_5 = MqttUpload("verkehr/sck_verkehr_5", self.mqtt_client, verbose=True)

        traffic_5 = TrafficCount("RH 5", "durchfahrt", Pin(28, Pin.IN), mqtt_traffic_5, verbose=True)
        self.actors.append(traffic_5)

    def _init_environment(self):
        self.weather = Weather("weather",
                               MultiplexedI2cSensor(BME280, multiplexer=self.mux74, channel=3), interval=10)
        self.actors.append(self.weather)

        self.weather_upload = MqttUploadActor("umwelt", self.mqtt_client, self.weather.status, interval=30, verbose=True)
        self.actors.append(self.weather_upload)

        self.light = Light("light", MultiplexedI2cSensor(GY302, multiplexer=self.mux74, channel=3), interval=10)
        self.actors.append(self.light)

        self.light_upload = MqttUploadActor("licht", self.mqtt_client, self.light.status, interval=10, verbose=True)
        self.actors.append(self.light_upload)

    def _init_multiplexers(self):
        # Name includes address for better reference
        self.mux70 = TCA9548A(self.i2c1, address=0x70)
        self.mux72 = TCA9548A(self.i2c1, address=0x72)
        self.mux74 = TCA9548A(self.i2c0, address=0x74)

