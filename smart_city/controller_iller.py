# This is the third Raspi of our MOC of the City of Kempten
# It implements the Illerufer (second base plate), nearby the river, with a Parking Area (including display),
# three waste containers and one traffic light

import asyncio

from device.driver.tca9548a import TCA9548A
from device.driver.gy302 import GY302
from device.driver.vl53l0x import VL53L0X
from device.multiplexed_i2c_sensor import MultiplexedI2cSensor
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from domain.waste.container import WasteContainer
from report.parking_area_panel import ParkingAreaPanelSH1106
from smart_city.controller_base import ControllerBase
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper


class ControllerIller(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Illerufer"

        self.actors = []

        self.actors.append(Heartbeat(verbose=True))
        self.actors.append(Housekeeper(verbose=False))

        self.mux1 = TCA9548A(self.i2c1, address=0x70)
        p1 = ParkingSpace("Illerufer 1", MultiplexedI2cSensor("Illerufer P1", VL53L0X, multiplexer=self.mux1, channel=5),
                          empty_threshold=50, verbose=False)
        p2 = ParkingSpace("Illerufer 2", MultiplexedI2cSensor("Illerufer P2", VL53L0X, multiplexer=self.mux1, channel=4),
                          empty_threshold=100, verbose=False)
        p3 = ParkingSpace("Illerufer 3", MultiplexedI2cSensor("Illerufer P3", VL53L0X, multiplexer=self.mux1, channel=3),
                          empty_threshold=65, verbose=False)
        p4 = ParkingSpace("Illerufer 4", MultiplexedI2cSensor("Illerufer P4", VL53L0X, multiplexer=self.mux1, channel=2),
                          empty_threshold=50, verbose=False)
        p5 = ParkingSpace("Illerufer 5", MultiplexedI2cSensor("Illerufer P5", VL53L0X, multiplexer=self.mux1, channel=1),
                          empty_threshold=50, verbose=False)
        p6 = ParkingSpace("Illerufer 6", MultiplexedI2cSensor("Illerufer P6", VL53L0X, multiplexer=self.mux1, channel=0),
                          empty_threshold=40, verbose=False)

        self.parking = ParkingArea("Illerufer", [p1, p2, p3, p4, p5, p6])
        self.actors.append(self.parking)

        self.parking_panel_large = ParkingAreaPanelSH1106(self.i2c0, self.parking, verbose=False)
        self.actors.append(self.parking_panel_large)

        self.mux3 = TCA9548A(self.i2c1, address=0x72)

        w1 = WasteContainer("Illerufer 1", MultiplexedI2cSensor("Illerufer Müll 1", GY302, multiplexer=self.mux3, channel=0), verbose=True)
        self.actors.append(w1)
        w2 = WasteContainer("Illerufer 2", MultiplexedI2cSensor("Illerufer Müll 2", GY302, multiplexer=self.mux3, channel=1), verbose=True)
        self.actors.append(w2)
        w3 = WasteContainer("Illerufer 3", MultiplexedI2cSensor("Illerufer Müll 3", GY302, multiplexer=self.mux3, channel=2), verbose=True)
        self.actors.append(w3)
        self.waste = [w1, w2, w3]

    def print_debug_log(self):
        number_of_empty_spaces = self.parking.number_of_empty_spaces()
        number_of_spaces = self.parking.number_of_spaces()
        parking_lots = "{:1d} / {:1d}".format(number_of_empty_spaces, number_of_spaces)
        print(parking_lots)
        for waste in self.waste:
            print("Waste {:s} {:s}".format(waste.actor_id, "full" if waste.full() else "OK"))

    async def create_tasks(self):
        print("create_tasks()")
        tasks = []
        for actor in self.actors:
            tasks.append(asyncio.create_task(actor.run()))
