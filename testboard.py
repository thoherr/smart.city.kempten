import micropython

from sensor.domain.parking.area import ParkingArea
from sensor.domain.parking.space import ParkingSpace

micropython.alloc_emergency_exception_buf(100)

from machine import Pin, I2C
import time

from sensor.device.vl53l0x import VL53L0X
from sensor.device.gy302 import GY302
from display.ssd1306 import SSD1306_I2C

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
tof = VL53L0X(i2c1)

budget = tof.measurement_timing_budget_us
print("Budget was:", budget)
tof.set_measurement_timing_budget(40000)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

display = SSD1306_I2C(128, 32, i2c1)

traffic_pin = Pin(14, Pin.IN)
traffic = Traffic(traffic_pin)
p1 = ParkingSpace(tof, 150)
parking = ParkingArea([p1])

while True:
    traffic.check()
    parking.check()
    light_value = "Light {:7.2f} lx".format(light.value())
    reed_value = "Reed value {:1d}".format(reed.value())
    tof_value = "Distance {:4d} mm".format(tof.value())
    traffic_count = "Traffic {:1d}".format(traffic.get_count())
    parking_lots = "Avail. Park. {:1d}".format(parking.number_of_empty_spaces())

    print(light_value)
    print(reed_value)
    print(tof_value)
    print(traffic_count)
    print(parking_lots)

    display.fill(0)                         # fill entire screen with colour=0
    display.text(light_value, 0, 0, 1)
    #display.text(reed_value, 0, 12, 1)
    display.text(traffic_count, 0, 12, 1)
    display.text(parking_lots, 0, 24, 1)
    display.show()

    time.sleep(0.1)
