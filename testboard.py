import micropython

from sensor.domain.parking.area import ParkingArea
from sensor.domain.parking.space import ParkingSpace

micropython.alloc_emergency_exception_buf(100)

from machine import Pin, I2C
import time

from sensor.device.tca9548a import TCA9548A
from sensor.device.vl53l0x import VL53L0X
from sensor.device.gy302 import GY302
from display.ssd1306 import SSD1306_I2C
from display.writer import Writer
import display.freesans20


from sensor.domain.traffic import Traffic

i2c0 = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
i2c1 = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)

print('Scan I2C Bus 0...')
devices = i2c0.scan()
if len(devices) == 0:
    print('Kein I2C-Gerät an I2C 0 gefunden!')
else:
    print('I2C-Geräte gefunden:', len(devices))
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))

print('Scan I2C Bus 1...')
devices = i2c1.scan()
if len(devices) == 0:
    print('Kein I2C-Gerät an I2C 1 gefunden!')
else:
    print('I2C-Geräte gefunden:', len(devices))
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))


led = Pin("LED", Pin.OUT)
reed = Pin(15, Pin.IN, Pin.PULL_DOWN)

light = GY302(i2c1)

multiplexer = TCA9548A(i2c1)
p0 = ParkingSpace(multiplexer, 0, VL53L0X)
p2 = ParkingSpace(multiplexer, 2, VL53L0X)
parking = ParkingArea([p0, p2], "Illerufer")

screen = SSD1306_I2C(128, 32, i2c1)

writer = Writer(screen, display.freesans20)

traffic_pin = Pin(14, Pin.IN)
traffic = Traffic(traffic_pin)

while True:
    traffic.check()
    parking.check()
    light_value = "Light {:7.2f} lx".format(light.value())
    reed_value = "Reed value {:1d}".format(reed.value())
    multiplexer.switch_to_channel(0)
    traffic_count = "Traffic {:1d}".format(traffic.get_count())
    number_of_empty_spaces = parking.number_of_empty_spaces()
    number_of_spaces = parking.number_of_spaces()
    parking_lots = "{:1d} / {:1d}".format(number_of_empty_spaces, number_of_spaces)
    parking_status = "{:6s}".format("  FREI" if number_of_empty_spaces > 0 else "BELEGT")

    print(light_value)
    print(reed_value)
    print(traffic_count)
    print(parking_lots)

    screen.fill(0)                         # fill entire screen with colour=0
    screen.text("Parkplatz", 0, 0, 1)
    screen.text(parking.name, 0, 12, 1)
    #screen.text(parking_lots, 88, 0, 1)
    if number_of_empty_spaces > 0:
        writer.set_textpos(screen, 0, 108)
        writer.printstring("{:1d}".format(number_of_empty_spaces))
    screen.text(parking_status, 80, 24, 1)
    screen.show()

    time.sleep(0.25)
