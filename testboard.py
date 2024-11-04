from machine import Pin, I2C
import time

from sensor.device.vl53l0x import VL53L0X
from sensor.device.gy302 import GY302
from display.ssd1306 import SSD1306_I2C

i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)

print('Scan I2C Bus...')
devices = i2c.scan()

if len(devices) == 0:
    print('Kein I2C-Gerät gefunden!')
else:
    print('I2C-Geräte gefunden:', len(devices))
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))


led = Pin("LED", Pin.OUT)

reed = Pin(15, Pin.IN, Pin.PULL_DOWN)

light = GY302(i2c)
tof = VL53L0X(i2c)

budget = tof.measurement_timing_budget_us
print("Budget was:", budget)
tof.set_measurement_timing_budget(40000)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

display = SSD1306_I2C(128, 32, i2c)

while True:
    light_value = "Light {:7.2f} lx".format(light.value())
    reed_value = "Reed value {:1d}".format(reed.value())
    tof_value = "Distance {:4d} mm".format(tof.value())

    print(light_value)
    print(reed_value)
    print(tof_value)

    display.fill(0)                         # fill entire screen with colour=0
    display.text(light_value, 0, 1, 1)
    display.text(reed_value, 0, 12, 1)
    display.text(tof_value, 0, 24, 1)
    display.show()

    led.toggle()
    time.sleep(0.25)
