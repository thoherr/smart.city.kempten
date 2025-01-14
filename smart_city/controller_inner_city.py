# This is the first Raspi of or MOC of the City of Kempten
# It implements the Innenstadt, around the Rathaus, with a Parking Area (including display),
# three waste containers and two traffic lights

import asyncio

from device.multiplexer.tca9548a import TCA9548A
from device.sensor.vl53l0x import VL53L0X
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from report.parking import ParkingAreaPanelSH1106
from smart_city.controller_base import ControllerBase
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper


class ControllerInnerCity(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Innenstadt"
        self.multiplexer = TCA9548A(self.i2c1)
        p1 = ParkingSpace("Rathaus 1", self.multiplexer, 0, VL53L0X, empty_threshold=50, verbose=True)
        p2 = ParkingSpace("Rathaus 2", self.multiplexer, 1, VL53L0X, empty_threshold=100, verbose=True)
        p3 = ParkingSpace("Rathaus 3", self.multiplexer, 2, VL53L0X, empty_threshold=65, verbose=True)
        p4 = ParkingSpace("Rathaus 4", self.multiplexer, 3, VL53L0X, empty_threshold=50, verbose=True)
        p5 = ParkingSpace("Rathaus 5", self.multiplexer, 4, VL53L0X, empty_threshold=50, verbose=True)
        p6 = ParkingSpace("Rathaus 6", self.multiplexer, 5, VL53L0X, empty_threshold=40, verbose=True)
        self.parking = ParkingArea("Rathaus", [p1, p2, p3, p4, p5, p6])
        self.parking_panel_large = ParkingAreaPanelSH1106(self.i2c0, self.parking, verbose=True)

    def print_debug_log(self):
        number_of_empty_spaces = self.parking.number_of_empty_spaces()
        number_of_spaces = self.parking.number_of_spaces()
        parking_lots = "{:1d} / {:1d}".format(number_of_empty_spaces, number_of_spaces)
        print(parking_lots)

    async def create_tasks(self):
        return asyncio.gather(asyncio.create_task(Heartbeat(print_timestamp=True).run()),
                              asyncio.create_task(Housekeeper(verbose=True).run()),
                              asyncio.create_task(self.parking.run()),
                              asyncio.create_task(self.parking_panel_large.run()))
