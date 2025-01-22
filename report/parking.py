import device.display.freesans20
import device.display.freesansbold40
from device.display.sh1106 import SH1106_I2C
from device.display.ssd1306 import SSD1306_I2C
from device.display.writer import Writer
from util.actor import Actor


class ParkingAreaPanel(Actor):
    def __init__(self, i2c, parking_area, interval=1, verbose=False):
        super().__init__("ParkingAreaPanel {:s}".format(parking_area.location), interval, verbose)
        self._screen = None
        self._writer_small = None
        self._writer_large = None
        self._width : int = -1
        self._status_y : int = -1
        self._i2c = i2c
        self._parking_area = parking_area
        self._counter = 0

    async def work(self):
        self.log("ParkingAreaPanel counter: {}".format(self._counter))
        number_of_empty_spaces = self._parking_area.number_of_empty_spaces()
        parking_lots_available = "{:1d}".format(number_of_empty_spaces)
        if self._verbose:
            self.log("{:1d} / {:1d}".format(number_of_empty_spaces, self._parking_area.number_of_spaces()))
        if self._counter < 5:
            parking_status = "{:s}".format("FREI" if number_of_empty_spaces > 0 else "BELEGT")
            self.display_text_panel(number_of_empty_spaces, parking_lots_available, parking_status)
        else:
            self.display_graphic_panel(parking_lots_available)
        if self._counter >= 8:
            self._counter = 0
        self._counter = self._counter + 1

    def display_text_panel(self, number_of_empty_spaces, parking_lots_available, parking_status):
        self._screen.fill(0)
        self._writer_small.set_textpos(self._screen, 0, 0)
        self._writer_small.printstring("Parkplatz\n{:s}".format(self._parking_area.location))
        if number_of_empty_spaces > 0:
            self._writer_large.set_textpos(self._screen, 0, self._width - self._writer_large.stringlen(parking_lots_available))
            self._writer_large.printstring(parking_lots_available)
        self._writer_small.set_textpos(self._screen, self._status_y, self._width - self._writer_small.stringlen(parking_status))
        self._writer_small.printstring(parking_status)
        self._screen.show()

    def display_graphic_panel(self, parking_lots_available):
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
        self._screen.hline(h_offset+h_size*i, v_offset_1, h_size, 0xffffff)
        self._screen.vline(h_offset+h_size*i, v_offset_2, v_size, 0xffffff)
        self._screen.vline(h_offset+h_size*(i+1), v_offset_2, v_size, 0xffffff)
        if not empty:
            self._screen.line(h_offset+h_size*i, v_offset_2, h_offset+h_size*(i+1), v_offset_2+v_size, 0xffffff)
            self._screen.line(h_offset+h_size*i, v_offset_2+v_size, h_offset+h_size*(i+1), v_offset_2, 0xffffff)


class ParkingAreaPanelSH1106(ParkingAreaPanel):
    def __init__(self, i2c, parking_area, interval=1, verbose=False):
        super().__init__(i2c, parking_area, interval, verbose)

        self._width = 128
        self._height = 64
        self._status_y = 44
        self._screen = SH1106_I2C(self._width, self._height, i2c)
        self._writer_small = Writer(self._screen, device.display.freesans20)
        self._writer_large = Writer(self._screen, device.display.freesansbold40)


class ParkingAreaPanelSSD1306(ParkingAreaPanel):
    def __init__(self, i2c, parking_area, interval=1, verbose=False):
        super().__init__(i2c, parking_area, interval, verbose)

        self._width = 128
        self._height = 64
        self._status_y = 24
        self._screen = SSD1306_I2C(self._width, self._height, i2c)
        self._writer_small = Writer(self._screen, device.display.freesans20)
        self._writer_large = Writer(self._screen, device.display.freesans20)
