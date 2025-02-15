import device.display.freesans20
from device.display.sh1106 import SH1106_I2C
from device.display.writer import Writer
from util.actor import Actor


class EnvironmentPanel(Actor):
    def __init__(self, actor_id, i2c, weather, light, multiplexer=None, interval=1, verbose=False):
        super().__init__(actor_id, interval, verbose)
        self._width = 128
        self._height = 64
        self._screen = SH1106_I2C(self._width, self._height, i2c)
        self._writer = Writer(self._screen, device.display.freesans20)
        self._i2c = i2c
        self._multiplexer = multiplexer
        self._weather = weather
        self._light = light

    async def work(self):
        temperature = self._weather.temperature()
        pressure = self._weather.pressure()
        humidity = self._weather.humidity()
        light = self._light.light()
        if self._verbose:
            self.log(f"Temperature {temperature:.1f}, Pressure {pressure:.1f}, Humidity {humidity:.1f}, Light {light:.0f}")
        if self._multiplexer:
            self._multiplexer.ensure_channel()
        self.show_info_screen(temperature, pressure, humidity, light)
        if self._multiplexer:
            self._multiplexer.reset_channel()

    def show_info_screen(self, temperature, pressure, humidity, light):
        self._screen.fill(0)
        temp_str = f"{temperature:.1f}°C"
        self._writer.set_textpos(self._screen, 0, 0)
        self._writer.printstring(temp_str)
        press_str = f"{pressure:.1f}hP"
        self._writer.set_textpos(self._screen, 30, 0)
        self._writer.printstring(press_str)
        hum_str = f"{humidity:.1f}%"
        self._writer.set_textpos(self._screen, 0, self._width - self._writer.stringlen(hum_str))
        self._writer.printstring(hum_str)
        light_str = f"{light:.0f}lx"
        self._writer.set_textpos(self._screen, 30, self._width - self._writer.stringlen(light_str))
        self._writer.printstring(light_str)
        self._screen.show()
