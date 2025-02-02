'''
Testing graphics on TFT display with ST7735 controller connected to Raspberry Pi Pico
'''

from device.display.st7735 import TFT
from device.display.st7735 import petme128font, seriffont, sysfont, terminalfont
from machine import SPI, Pin
import time


def tftprinttest(fonts, il):
    tft.fill(TFT.BLACK);
    tft.rotation(3);
    v = 0
    for i in range(len(fonts)):
        font = fonts[i];
        tft.text((0, v), f"{i + 1} - Hello World!", TFT.RED, font, 1, nowrap=True)
        v += font["Height"]
    large_font = fonts[il];
    tft.text((0, v), f"Font {il + 1}", TFT.BLUE, large_font, 4, nowrap=True)
    v += large_font["Height"] * 4
    tft.text((0, v), str(1234.567), TFT.BLUE, large_font, 4, nowrap=True)
    v += large_font["Height"] * 4
    tft.text((0, v), "Hello, world!", TFT.BLUE, large_font, 4, nowrap=True)


def test_main():
    fonts = [petme128font.petme128font, seriffont.seriffont, sysfont.sysfont, terminalfont.terminalfont]
    i = 0
    while True:
        tftprinttest(fonts, i)
        i = (i + 1) % len(fonts)
        time.sleep_ms(1500)


print(__name__)

if __name__ == "test_st7735":
    spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(10), mosi=Pin(11), miso=None)
    tft = TFT(spi, 16, 17, 18)
    tft.initr()
    #    tft.rgb(True)
    test_main()
