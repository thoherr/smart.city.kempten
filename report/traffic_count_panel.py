import device.display.freesans20
from device.display.ssd1306 import SSD1306_I2C
from device.display.writer import Writer
from util.actor import Actor


class TrafficCountPanel(Actor):
    def __init__(self, actor_id, i2c, traffic_counters, interval=1, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._width = 128
        self._height = 32
        self._status_y = 16
        self._screen = SSD1306_I2C(self._width, self._height, i2c)
        self._writer = Writer(self._screen, device.display.freesans20)
        self._i2c = i2c
        self._traffic_counters = traffic_counters

    async def work(self):
        west = self._traffic_counters[0].value()
        east = self._traffic_counters[1].value()
        if self._verbose:
            self.log("<-- {:1d} / {:1d} -->".format(west, east))
        self.show_info_screen(west, east)

    def show_info_screen(self, west, east):
        self._screen.fill(0)
        self._writer.set_textpos(self._screen, 0, 0)
        self._writer.printstring("<-- {:d}".format(west))
        east_text = "{:d} -->".format(east)
        self._writer.set_textpos(self._screen, 12,
                                 self._width - self._writer.stringlen(east_text))
        self._writer.printstring(east_text)
        self._screen.show()
