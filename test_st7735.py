'''
Testing graphics on TFT display with ST7735 controller connected to Raspberry Pi Pico
'''

from device.display.st7735 import TFT
from device.display.st7735 import sysfont, seriffont, terminalfont
from machine import SPI,Pin
import time


def tftprinttest(font1, font2, font3):
    tft.fill(TFT.BLACK);
    tft.rotation(3);
    v = 30
    tft.text((0, v), "Hello World!", TFT.RED, font1, 1, nowrap=True)
    v += font1["Height"]
    tft.text((0, v), "Hello World!", TFT.RED, font2, 1, nowrap=True)
    v += font2["Height"]
    tft.text((0, v), "Hello World!", TFT.YELLOW, font3, 2, nowrap=True)
    v += font3["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.PURPLE, font2, 3, nowrap=True)
    v += font2["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, font3, 4, nowrap=True)
    time.sleep_ms(1500)

def test_main():
    tftprinttest(sysfont.sysfont, seriffont.seriffont, terminalfont.terminalfont)
    time.sleep_ms(100)

print(__name__)

if __name__ == "test_st7735":
    spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(10), mosi=Pin(11), miso=None)
    tft=TFT(spi,16,17,18)
    tft.initr()
#    tft.rgb(True)
    test_main()
