from array import array

import device.display.font6
import device.display.font10
import device.display.freesans20
import device.display.freesansbold40
from device.display.sh1106 import SH1106_I2C
from device.display.ssd1306 import SSD1306_I2C
from device.display.writer import Writer
from domain.parking.area import ParkingArea
from domain.waste.area import WasteArea
from util.actor import Actor


class ParkingAreaPanel(Actor):
    def __init__(self, i2c, parking_area, interval=1, verbose=False):
        super().__init__("ParkingAreaPanel {:s}".format(parking_area.location), interval, verbose)
        self._screen = None
        self._writer_small = None
        self._writer_large = None
        self._width: int = -1
        self._status_y: int = -1
        self._i2c = i2c
        self._parking_area = parking_area

    async def work(self):
        number_of_empty_spaces = self._parking_area.number_of_empty_spaces()
        parking_lots_available = "{:1d}".format(number_of_empty_spaces)
        parking_status = "{:s}".format("FREI" if number_of_empty_spaces > 0 else "BELEGT")
        if self._verbose:
            self.log("{:1d} / {:1d}".format(number_of_empty_spaces, self._parking_area.number_of_spaces()))
        self.show_info_screen(number_of_empty_spaces, parking_lots_available, parking_status)

    def show_info_screen(self, number_of_empty_spaces, parking_lots_available, parking_status):
        raise NotImplementedError("DisplayInfoPanel not implemented by child class")

    def show_text_screen(self, number_of_empty_spaces, parking_lots_available, parking_status):
        self._screen.fill(0)
        self._writer_small.set_textpos(self._screen, 0, 0)
        self._writer_small.printstring("Parkplatz\n{:s}".format(self._parking_area.location))
        if number_of_empty_spaces > 0:
            self._writer_large.set_textpos(self._screen, 0,
                                           self._width - self._writer_large.stringlen(parking_lots_available))
            self._writer_large.printstring(parking_lots_available)
        self._writer_small.set_textpos(self._screen, self._status_y,
                                       self._width - self._writer_small.stringlen(parking_status))
        self._writer_small.printstring(parking_status)
        self._screen.show()

    def show_graphic_screen(self, parking_lots_available):
        self._screen.fill(0)
        self._writer_large.set_textpos(self._screen, 32, 16)
        self._writer_large.printstring(parking_lots_available)
        for i in range(self._parking_area.number_of_spaces()):
            self.draw_slot(i, self._parking_area.spaces[i].empty())
        self._screen.show()

    def draw_slot(self, slot_number, empty):
        if slot_number <= 5:
            i = slot_number
            h_offset = 16
            h_size = 16
            v_offset_1 = 0
            v_offset_2 = 0
            v_size = 28
        elif slot_number <= 7:
            i = slot_number - 6
            h_offset = 56
            h_size = 28
            v_offset_1 = 63
            v_offset_2 = 50
            v_size = 13
        else:
            return
        self._screen.hline(h_offset + h_size * i, v_offset_1, h_size, 0xffffff)
        self._screen.vline(h_offset + h_size * i, v_offset_2, v_size, 0xffffff)
        self._screen.vline(h_offset + h_size * (i + 1), v_offset_2, v_size, 0xffffff)
        if not empty:
            self._screen.line(h_offset + h_size * i, v_offset_2, h_offset + h_size * (i + 1), v_offset_2 + v_size,
                              0xffffff)
            self._screen.line(h_offset + h_size * i, v_offset_2 + v_size, h_offset + h_size * (i + 1), v_offset_2,
                              0xffffff)


class ParkingAreaPanelSH1106(ParkingAreaPanel):
    text_cycles = 5
    graphics_cycles = 2
    waste_cycles = 2

    def __init__(self, i2c, parking_area : ParkingArea, waste_area : WasteArea, interval=1, verbose=False):
        super().__init__(i2c, parking_area, interval, verbose)
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


class ParkingAreaPanelSSD1306(ParkingAreaPanel):
    def __init__(self, i2c, parking_area, interval=1, verbose=False):
        super().__init__(i2c, parking_area, interval, verbose)

        self._width = 128
        self._height = 32
        self._status_y = 16
        self._screen = SSD1306_I2C(self._width, self._height, i2c)
        self._writer_small = Writer(self._screen, device.display.font6)
        self._writer_large = Writer(self._screen, device.display.font10)

    def show_info_screen(self, number_of_empty_spaces, parking_lots_available, parking_status):
        self.show_text_screen(number_of_empty_spaces, parking_lots_available, parking_status)
