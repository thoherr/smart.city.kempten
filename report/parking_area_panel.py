from domain.parking.area import ParkingArea
from util.actor import Actor


class ParkingAreaPanel(Actor):
    def __init__(self, i2c, parking_area : ParkingArea, multiplexer=None, interval=1, verbose=False):
        super().__init__("ParkingAreaPanel {:s}".format(parking_area.location), interval, verbose)
        self._screen = None
        self._writer_small = None
        self._writer_large = None
        self._width: int = -1
        self._status_y: int = -1
        self._i2c = i2c
        self._multiplexer = multiplexer
        self._parking_area = parking_area

    async def work(self):
        number_of_empty_spaces = self._parking_area.number_of_empty_spaces()
        parking_lots_available = "{:1d}".format(number_of_empty_spaces)
        parking_status = "{:s}".format("FREI" if number_of_empty_spaces > 0 else "BELEGT")
        if self._verbose:
            self.log("{:1d} / {:1d}".format(number_of_empty_spaces, self._parking_area.number_of_spaces()))
        if self._multiplexer:
            self._multiplexer.ensure_channel()
        self.show_info_screen(number_of_empty_spaces, parking_lots_available, parking_status)
        if self._multiplexer:
            self._multiplexer.reset_channel()

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
