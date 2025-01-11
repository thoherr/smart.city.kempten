import asyncio

from device.sensor.vl53l0x import VL53L0X
from report.parking import ParkingAreaPanel
from util.heartbeat import Heartbeat
from device.multiplexer.tca9548a import TCA9548A
from domain.parking.area import ParkingArea
from domain.parking.space import ParkingSpace
from smart_city.controller_base import ControllerBase


class ControllerOne(ControllerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Innenstadt"
        self.multiplexer = TCA9548A(self.i2c1)
        p0 = ParkingSpace(self.multiplexer, 0, VL53L0X)
        p2 = ParkingSpace(self.multiplexer, 2, VL53L0X)
        self.parking = ParkingArea("Illerufer", [p0, p2, p0, p2, p0, p2, p0, p2, p0, p2, p0, p2])
        self.parking_panel = ParkingAreaPanel(self.i2c0, self.parking)

    def print_debug_log(self):
        number_of_empty_spaces = self.parking.number_of_empty_spaces()
        number_of_spaces = self.parking.number_of_spaces()
        parking_lots_available = "{:1d}".format(number_of_empty_spaces)
        parking_lots = "{:1d} / {:1d}".format(number_of_empty_spaces, number_of_spaces)
        parking_status = "{:6s}".format("  FREI" if number_of_empty_spaces > 0 else "BELEGT")
        print(parking_lots)


    async def create_tasks(self):
        return asyncio.gather(asyncio.create_task(Heartbeat(print_timestamp=True).run()),
                             asyncio.create_task(self.parking.run()),
                              asyncio.create_task(self.parking_panel.run()))


