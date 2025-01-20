# This is the first Raspi of or MOC of the City of Kempten
# It implements the Innenstadt, around the Rathaus, with a Parking Area (including display),
# three waste containers and two traffic lights

import asyncio

from device.multiplexer.tca9548a import TCA9548A
from device.sensor.gy302 import GY302
from device.sensor.vl53l0x import VL53L0X
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from domain.waste.container import WasteContainer
from report.parking import ParkingAreaPanelSH1106
from smart_city.controller_base import ControllerBase
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper


class ControllerInnerCity(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Innenstadt"

        self.actors = []

        self.actors.append(Heartbeat(verbose=True))
        self.actors.append(Housekeeper(verbose=False))

        self.mux1 = TCA9548A(self.i2c1, address=0x70)
        p1 = ParkingSpace("Rathaus 1", self.mux1.i2c, VL53L0X, multiplexer=self.mux1, channel=5,
                          empty_threshold=50, verbose=False)
        p2 = ParkingSpace("Rathaus 2", self.mux1.i2c, VL53L0X, multiplexer=self.mux1, channel=4,
                          empty_threshold=100, verbose=False)
        p3 = ParkingSpace("Rathaus 3", self.mux1.i2c, VL53L0X, multiplexer=self.mux1, channel=3,
                          empty_threshold=65, verbose=False)
        p4 = ParkingSpace("Rathaus 4", self.mux1.i2c, VL53L0X, multiplexer=self.mux1, channel=2,
                          empty_threshold=50, verbose=False)
        p5 = ParkingSpace("Rathaus 5", self.mux1.i2c, VL53L0X, multiplexer=self.mux1, channel=1,
                          empty_threshold=50, verbose=False)
        p6 = ParkingSpace("Rathaus 6", self.mux1.i2c, VL53L0X, multiplexer=self.mux1, channel=0,
                          empty_threshold=40, verbose=False)

        self.mux2 = TCA9548A(self.i2c1, address=0x71)
        p7 = ParkingSpace("Rathaus 7", self.mux2.i2c, VL53L0X, multiplexer=self.mux2, channel=7,
                          empty_threshold=50, verbose=False)
        p8 = ParkingSpace("Rathaus 8", self.mux2.i2c, VL53L0X, multiplexer=self.mux2, channel=1,
                          empty_threshold=50, verbose=False)

        self.parking = ParkingArea("Rathaus", [p1, p2, p3, p4, p5, p6, p7, p8])
        self.actors.append(self.parking)

        self.parking_panel_large = ParkingAreaPanelSH1106(self.i2c0, self.parking, verbose=False)
        self.actors.append(self.parking_panel_large)

        self.mux3 = TCA9548A(self.i2c1, address=0x72)

        w1 = WasteContainer("Rathaus 1", self.mux3.i2c, GY302, multiplexer=self.mux3, channel=0, verbose=True)
        self.actors.append(w1)
        w2 = WasteContainer("Rathaus 2", self.mux3.i2c, GY302, multiplexer=self.mux3, channel=1, verbose=True)
        self.actors.append(w2)
        w3 = WasteContainer("Rathaus 3", self.mux3.i2c, GY302, multiplexer=self.mux3, channel=2, verbose=True)
        self.actors.append(w3)
        self.waste = [w1, w2, w3]

    def print_debug_log(self):
        number_of_empty_spaces = self.parking.number_of_empty_spaces()
        number_of_spaces = self.parking.number_of_spaces()
        parking_lots = "{:1d} / {:1d}".format(number_of_empty_spaces, number_of_spaces)
        print(parking_lots)
        for waste in self.waste:
            print("Waste {:s} {:s}".format(waste.id, "full" if waste.full() else "OK"))

    async def create_tasks(self):
        print("create_tasks()")
        tasks = []
        for actor in self.actors:
            tasks.append(asyncio.create_task(actor.run()))
