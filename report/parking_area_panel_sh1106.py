from uarray import array

import device.display.freesans20
import device.display.freesansbold40
from device.display.sh1106 import SH1106_I2C
from device.display.writer import Writer
from domain.parking.area import ParkingArea
from domain.waste.area import WasteArea
from report.parking_area_panel import ParkingAreaPanel


class ParkingAreaPanelSH1106(ParkingAreaPanel):
    text_cycles = 5
    graphics_cycles = 2
    waste_cycles = 2

    def __init__(self, i2c, parking_area: ParkingArea, waste_area: WasteArea, multiplexer=None, interval=1, verbose=False):
        super().__init__(i2c, parking_area, multiplexer, interval, verbose)
        self._waste_containers = waste_area.containers

        self._width = 128
        self._height = 64
        self._status_y = 44
        self._screen = SH1106_I2C(self._width, self._height, i2c)
        self._writer_small = Writer(self._screen, device.display.freesans20)
        self._writer_large = Writer(self._screen, device.display.freesansbold40)
        self._counter = 0

    def show_info_screen(self, number_of_empty_spaces, parking_lots_available, parking_status):
        if self._verbose:
            self.log("ParkingAreaPanelSH1106 counter: {}".format(self._counter))
        if self._counter < self.text_cycles:
            self.show_text_screen(number_of_empty_spaces, parking_lots_available, parking_status)
        elif self._counter < self.text_cycles + self.graphics_cycles:
            self.show_graphic_screen(parking_lots_available)
        else:
            self.show_waste_screen()
        if self._counter >= self.text_cycles + self.graphics_cycles + self.waste_cycles:
            self._counter = 0
        self._counter = self._counter + 1

    def show_waste_screen(self):
        self._screen.fill(0)
        for i in range(len(self._waste_containers)):
            self.draw_waste_bin(i, self._waste_containers[i].full())
        self._screen.show()

    def draw_waste_bin(self, slot, is_full):
        self._writer_small.set_textpos(self._screen, 0, 0)
        self._writer_small.printstring("Smart Waste")
        x_offset = 16
        y_offset = 30
        bin_width = 24
        bin_slope_width = 2
        x_distance = 32
        bin_height = 32
        coords = array('h', [0, 0,
                             bin_slope_width, bin_height,
                             bin_width - bin_slope_width, bin_height,
                             bin_width, 0])
        self._screen.poly(x_offset + x_distance * slot, y_offset, coords, 0xffffff, is_full)
