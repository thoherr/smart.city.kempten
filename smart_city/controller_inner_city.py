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

        self.actors.append(Heartbeat(print_timestamp=True))
        self.actors.append(Housekeeper(verbose=True))

        self.mux1 = TCA9548A(self.i2c1, address=0x70)
        p1 = ParkingSpace("Rathaus 1", self.mux1, 0, VL53L0X, empty_threshold=50, verbose=True)
        p2 = ParkingSpace("Rathaus 2", self.mux1, 1, VL53L0X, empty_threshold=100, verbose=True)
        p3 = ParkingSpace("Rathaus 3", self.mux1, 2, VL53L0X, empty_threshold=65, verbose=True)
        p4 = ParkingSpace("Rathaus 4", self.mux1, 3, VL53L0X, empty_threshold=50, verbose=True)
        p5 = ParkingSpace("Rathaus 5", self.mux1, 4, VL53L0X, empty_threshold=50, verbose=True)
        p6 = ParkingSpace("Rathaus 6", self.mux1, 5, VL53L0X, empty_threshold=40, verbose=True)
        self.parking = ParkingArea("Rathaus", [p1, p2, p3, p4, p5, p6])
        self.actors.append(self.parking)

        self.parking_panel_large = ParkingAreaPanelSH1106(self.i2c0, self.parking, verbose=True)
        self.actors.append(self.parking_panel_large)

        self.mux2 = TCA9548A(self.i2c1, address=0x71)

        w1 = WasteContainer("Rathaus 1", self.mux2, 0, GY302)
        self.actors.append(w1)
        w2 = WasteContainer("Rathaus 2", self.mux2, 1, GY302)
        self.actors.append(w2)
        w3 = WasteContainer("Rathaus 3", self.mux2, 2, GY302)
        self.actors.append(w3)
        self.waste = [w1, w2, w3]

    def print_debug_log(self):
        number_of_empty_spaces = self.parking.number_of_empty_spaces()
        number_of_spaces = self.parking.number_of_spaces()
        parking_lots = "{:1d} / {:1d}".format(number_of_empty_spaces, number_of_spaces)
        print(parking_lots)
        for waste in self.waste:
            print("Waste {:s} {:s}".format(waste.location, "full" if waste.full() else "OK"))

    async def create_tasks(self):
        return asyncio.gather(self.actors)
