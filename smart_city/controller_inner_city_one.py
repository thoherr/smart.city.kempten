# This is the first Raspi of our MOC of the City of Kempten
# It implements the first controller at Innenstadt, around the Rathaus, with a Parking Area (including display)
# and three waste containers

import setup_mqtt_config as mqtt_config
from device.driver.gy302 import GY302
from device.driver.tca9548a import TCA9548A
from device.driver.vl53l0x import VL53L0X
from device.multiplexed_i2c_sensor import MultiplexedI2cSensor
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from domain.waste.area import WasteArea
from domain.waste.container import WasteContainer
from report.mqtt_upload import MqttUpload
from report.parking_area_panel import ParkingAreaPanelSH1106
from smart_city.controller_base import ControllerBase


class ControllerInnerCityOne(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Innenstadt"

        self.mux1 = TCA9548A(self.i2c1, address=0x70)
        p1 = ParkingSpace("Rathaus 1", MultiplexedI2cSensor("Rathaus P1", VL53L0X, multiplexer=self.mux1, channel=5),
                          empty_threshold=40, verbose=True)
        p2 = ParkingSpace("Rathaus 2", MultiplexedI2cSensor("Rathaus P2", VL53L0X, multiplexer=self.mux1, channel=4),
                          empty_threshold=50, verbose=True)
        p3 = ParkingSpace("Rathaus 3", MultiplexedI2cSensor("Rathaus P3", VL53L0X, multiplexer=self.mux1, channel=3),
                          empty_threshold=50, verbose=True)
        p4 = ParkingSpace("Rathaus 4", MultiplexedI2cSensor("Rathaus P4", VL53L0X, multiplexer=self.mux1, channel=2),
                          empty_threshold=60, verbose=True)
        p5 = ParkingSpace("Rathaus 5", MultiplexedI2cSensor("Rathaus P5", VL53L0X, multiplexer=self.mux1, channel=1),
                          empty_threshold=100, verbose=True)
        p6 = ParkingSpace("Rathaus 6", MultiplexedI2cSensor("Rathaus P6", VL53L0X, multiplexer=self.mux1, channel=0),
                          empty_threshold=50, verbose=True)

        self.mux2 = TCA9548A(self.i2c1, address=0x71)
        p7 = ParkingSpace("Rathaus 7", MultiplexedI2cSensor("Rathaus P7", VL53L0X, multiplexer=self.mux2, channel=7),
                          empty_threshold=65, verbose=True)
        p8 = ParkingSpace("Rathaus 8", MultiplexedI2cSensor("Rathaus P8", VL53L0X, multiplexer=self.mux2, channel=1),
                          empty_threshold=50, verbose=True)

        self.parking = ParkingArea("Rathaus", [p1, p2, p3, p4, p5, p6, p7, p8])
        self.actors.append(self.parking)

        self.parking_upload = MqttUpload("sck_parkraum_1", self.mqtt_client,
                                       f"{mqtt_config.mqtt_topic_root}/parkraum/sck_parkraum_1",
                                       self.parking.status, interval=3, verbose=True)
        self.actors.append(self.parking_upload)

        self.mux3 = TCA9548A(self.i2c1, address=0x72)

        w1 = WasteContainer("Rathaus 1",
                            MultiplexedI2cSensor("Rathaus Müll 1", GY302, multiplexer=self.mux3, channel=0))
        self.actors.append(w1)
        w2 = WasteContainer("Rathaus 2",
                            MultiplexedI2cSensor("Rathaus Müll 2", GY302, multiplexer=self.mux3, channel=1))
        self.actors.append(w2)
        w3 = WasteContainer("Rathaus 3",
                            MultiplexedI2cSensor("Rathaus Müll 3", GY302, multiplexer=self.mux3, channel=2))
        self.actors.append(w3)
        self.waste = WasteArea("Rathaus", [w1, w2, w3])

        self.parking_and_waste_infopanel = ParkingAreaPanelSH1106(self.i2c0, self.parking, self.waste, verbose=False)
        self.actors.append(self.parking_and_waste_infopanel)

        self.waste_upload = MqttUpload("sck_smart_waste_1", self.mqtt_client,
                                       f"{mqtt_config.mqtt_topic_root}/smart_waste/sck_smart_waste_1",
                                       self.waste.status, interval=3, verbose=True)
        self.actors.append(self.waste_upload)
