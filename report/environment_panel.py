import device.display.freesans35
from device.display.sh1106 import SH1106_I2C
from device.display.writer import Writer
from util.actor import Actor


class EnvironmentPanel(Actor):
    def __init__(self, actor_id, i2c, weather, light, multiplexer=None, interval=2, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._width = 128
        self._height = 64
        self._screen = SH1106_I2C(self._width, self._height, i2c)
        self._writer = Writer(self._screen, device.display.freesans35)
        self._i2c = i2c
        self._multiplexer = multiplexer
        self._weather = weather
        self._light = light
        self._counter = 0

    async def work(self):
        temperature = self._weather.temperature()
        pressure = self._weather.pressure()
        humidity = self._weather.humidity()
        light = self._light.light()
        if self._verbose:
            self.log(f"Temperature {temperature:.1f}, Pressure {pressure:.0f}, Humidity {humidity:.1f}, Light {light:.0f}")
        if self._multiplexer:
            self._multiplexer.ensure_channel()
        self.show_info_screen(temperature, pressure, humidity, light)
        if self._multiplexer:
            self._multiplexer.reset_channel()

    def show_info_screen(self, temperature, pressure, humidity, light):
        self._screen.fill(0)

        if self._counter % 2 == 0:
            self.show_data(f"{temperature:.1f} C", f"{humidity:.1f} %")
        else:
            self.show_data(f"{pressure:.0f} hPa", f"{light:.0f} lux")

        self._counter = (self._counter + 1) % 2

        self._screen.show()

    def show_data(self, top_left, bottom_right):
        self._writer.set_textpos(self._screen, 0, 0)
        self._writer.printstring(top_left)
        self._writer.set_textpos(self._screen, 30, self._width - self._writer.stringlen(bottom_right))
        self._writer.printstring(bottom_right)
