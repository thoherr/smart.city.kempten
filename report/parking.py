import asyncio

import device.display.freesans20
import device.display.freesansbold40
from device.display.sh1106 import SH1106_I2C
from device.display.ssd1306 import SSD1306_I2C
from device.display.writer import Writer


class ParkingAreaPanel:
    def __init__(self, i2c, parking_area, interval=1):
        self._screen = None
        self._writer_small = None
        self._writer_large = None
        self._width : int = -1
        self._status_y : int = -1
        self._i2c = i2c
        self._parking_area = parking_area
        self._interval = interval

    async def run(self):
        while True:
            self.update_parking_panel()
            await asyncio.sleep(self._interval)

    def update_parking_panel(self):
        number_of_empty_spaces = self._parking_area.number_of_empty_spaces()
        parking_lots_available = "{:1d}".format(number_of_empty_spaces)
        parking_status = "{:s}".format("FREI" if number_of_empty_spaces > 0 else "BELEGT")
        self._screen.fill(0)
        self._writer_small.set_textpos(self._screen, 0, 0)
        self._writer_small.printstring("Parkplatz\n{:s}".format(self._parking_area.location))
        if number_of_empty_spaces > 0:
            self._writer_large.set_textpos(self._screen, 0, self._width - self._writer_large.stringlen(parking_lots_available))
            self._writer_large.printstring(parking_lots_available)
        self._writer_small.set_textpos(self._screen, self._status_y, self._width - self._writer_small.stringlen(parking_status))
        self._writer_small.printstring(parking_status)
        self._screen.show()


class ParkingAreaPanelSH1106(ParkingAreaPanel):
    def __init__(self, i2c, parking_area, interval=1):
        super().__init__(i2c, parking_area, interval)

        self._width = 128
        self._height = 64
        self._status_y = 44
        self._screen = SH1106_I2C(self._width, self._height, i2c)
        self._writer_small = Writer(self._screen, device.display.freesans20)
        self._writer_large = Writer(self._screen, device.display.freesansbold40)


class ParkingAreaPanelSSD1306(ParkingAreaPanel):
    def __init__(self, i2c, parking_area, interval=1):
        super().__init__(i2c, parking_area, interval)

        self._width = 128
        self._height = 64
        self._status_y = 24
        self._screen = SSD1306_I2C(self._width, self._height, i2c)
        self._writer_small = Writer(self._screen, device.display.freesans20)
        self._writer_large = Writer(self._screen, device.display.freesans20)
