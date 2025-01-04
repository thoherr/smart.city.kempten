import micropython

micropython.alloc_emergency_exception_buf(100)

from machine import Pin
import time

from traffic_light.column import Column as TrafficLightColumn
from traffic_light.crossing import Crossing as TrafficLightCrossing

led = Pin("LED", Pin.OUT)

l1 = TrafficLightColumn(9, 10, 11, 1)
l2 = TrafficLightColumn(14, 13, 12, 0)

crossing = TrafficLightCrossing([l1, l2])

while True:
    for i in range(100):
        led.toggle()
        crossing.next_tick()
        if i == 65:
            crossing.turn_on(TrafficLightCrossing.OUT_OF_ORDER_CIRCUIT)
        elif i == 75:
            crossing.turn_off()
        if i == 85:
            crossing.turn_on(TrafficLightCrossing.OUT_OF_ORDER_CIRCUIT)
        elif i == 99:
            crossing.turn_on()
        time.sleep(1)
