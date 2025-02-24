# This is the first Raspi of our MOC of the City of Kempten
# It implements the first controller at Innenstadt, around the Rathaus, with a Parking Area (including display)
# and three waste containers
import gc

from device.driver.gy302 import GY302
from device.driver.tca9548a import TCA9548A
from device.driver.vl53l0x import VL53L0X
from device.multiplexed_i2c_sensor import MultiplexedI2cSensor

gc.collect()

from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from domain.waste.area import WasteArea
from domain.waste.container import WasteContainer

gc.collect()

from report.mqtt_upload import MqttUploadActor
from report.parking_area_panel_sh1106 import ParkingAreaPanelSH1106
from smart_city.controller_base import ControllerBase

from setup_values import *

class ControllerInnerCityOne(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mux1 = TCA9548A(self.i2c1, address=0x70)
        p1 = ParkingSpace("Rathaus 1", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux1, channel=5),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=40, verbose=PARK_SENSOR_VERBOSITY)
        p2 = ParkingSpace("Rathaus 2", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux1, channel=4),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=50, verbose=PARK_SENSOR_VERBOSITY)
        p3 = ParkingSpace("Rathaus 3", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux1, channel=3),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=52, verbose=PARK_SENSOR_VERBOSITY)
        p4 = ParkingSpace("Rathaus 4", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux1, channel=2),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=60, verbose=PARK_SENSOR_VERBOSITY)
        p5 = ParkingSpace("Rathaus 5", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux1, channel=1),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=95, verbose=PARK_SENSOR_VERBOSITY)
        p6 = ParkingSpace("Rathaus 6", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux1, channel=0),
                          empty_threshold=40, verbose=PARK_SENSOR_VERBOSITY)

        self.mux2 = TCA9548A(self.i2c1, address=0x71)
        p7 = ParkingSpace("Rathaus 7", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux2, channel=7),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=70, verbose=PARK_SENSOR_VERBOSITY)
        p8 = ParkingSpace("Rathaus 8", MultiplexedI2cSensor(VL53L0X, multiplexer=self.mux2, channel=1),
                          interval=PARKING_SPACE_CHECK_INTERVAL,
                          empty_threshold=53, verbose=PARK_SENSOR_VERBOSITY)

        gc.collect()

        self.parking = ParkingArea("Rathaus", [p1, p2, p3, p4, p5, p6, p7, p8])
        self.actors.append(self.parking)

        self.parking_upload = MqttUploadActor("parkraum/sck_parkraum_1", self.mqtt_client, self.parking.status,
                                              interval=PARKRAUM_MQTT_INTERVAL)
        self.actors.append(self.parking_upload)

        self.mux3 = TCA9548A(self.i2c1, address=0x72)

        gc.collect()

        w1 = WasteContainer("Rathaus 1",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux3, channel=0),
                            interval=SMART_WASTE_CHECK_INTERVAL,
                            verbose=WASTE_SENSOR_VERBOSITY)
        self.actors.append(w1)
        w2 = WasteContainer("Rathaus 2",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux3, channel=1),
                            interval=SMART_WASTE_CHECK_INTERVAL,
                            verbose=WASTE_SENSOR_VERBOSITY)
        self.actors.append(w2)
        w3 = WasteContainer("Rathaus 3",
                            MultiplexedI2cSensor(GY302, multiplexer=self.mux3, channel=2),
                            interval=SMART_WASTE_CHECK_INTERVAL,
                            verbose=WASTE_SENSOR_VERBOSITY)
        self.actors.append(w3)
        self.waste = WasteArea("Rathaus", [w1, w2, w3])

        gc.collect()

        self.parking_and_waste_infopanel = ParkingAreaPanelSH1106(self.i2c0, self.parking, self.waste)
        self.actors.append(self.parking_and_waste_infopanel)

        self.waste_upload = MqttUploadActor("smart_waste/sck_smart_waste_1", self.mqtt_client, self.waste.status,
                                            interval=SMART_WASTE_MQTT_INTERVAL)
        self.actors.append(self.waste_upload)
