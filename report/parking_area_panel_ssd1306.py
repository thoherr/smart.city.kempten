import device.display.font10
import device.display.font6
from device.display.ssd1306 import SSD1306_I2C
from device.display.writer import Writer
from domain.parking.area import ParkingArea
from report.parking_area_panel import ParkingAreaPanel


class ParkingAreaPanelSSD1306(ParkingAreaPanel):
    def __init__(self, i2c, parking_area : ParkingArea, **kwargs):
        super(ParkingAreaPanelSSD1306, self).__init__(i2c, parking_area, **kwargs)

        self._width = 128
        self._height = 32
        self._status_y = 16
        self._screen = SSD1306_I2C(self._width, self._height, i2c)
        self._writer_small = Writer(self._screen, device.display.font6)
        self._writer_large = Writer(self._screen, device.display.font10)

    def show_info_screen(self, number_of_empty_spaces, parking_lots_available, parking_status):
        self.show_text_screen(number_of_empty_spaces, parking_lots_available, parking_status)
