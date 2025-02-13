import device.display.freesans35
from device.display.sh1106 import SH1106_I2C
from device.display.writer import Writer
from util.actor import Actor


class TrafficCountPanel(Actor):
    def __init__(self, actor_id, i2c, traffic_counters, multiplexer=None, interval=1, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._width = 128
        self._height = 64
        self._screen = SH1106_I2C(self._width, self._height, i2c)
        self._writer = Writer(self._screen, device.display.freesans35)
        self._i2c = i2c
        self._multiplexer = multiplexer
        self._traffic_counters = traffic_counters

    async def work(self):
        west = self._traffic_counters[0].value()
        east = self._traffic_counters[1].value()
        if self._verbose:
            self.log("<-- {:3d} / {:3d} -->".format(west, east))
        if self._multiplexer:
            self._multiplexer.ensure_channel()
        self.show_info_screen(west, east)
        if self._multiplexer:
            self._multiplexer.reset_channel()

    def show_info_screen(self, west, east):
        self._screen.fill(0)
        east_text = "--> {:d}".format(east)
        self._writer.set_textpos(self._screen, 30, self._width - self._writer.stringlen(east_text))
        self._writer.printstring(east_text)
        west_text = "{:d} <--".format(west)
        self._writer.set_textpos(self._screen, 0, 0)
        self._writer.printstring(west_text)
        self._screen.show()
