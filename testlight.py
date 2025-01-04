import micropython

micropython.alloc_emergency_exception_buf(100)

from machine import Pin
import time

from traffic_light.column import Column as TrafficLightColumn
from traffic_light.crossing import Crossing as TrafficLightCrossing

led = Pin("LED", Pin.OUT)

l1 = TrafficLightColumn(9, 10, 11, 1)
l2 = TrafficLightColumn(14, 13, 12, 0)

crossing = TrafficLightCrossing([l1, l2], TrafficLightCrossing.DEFAULT_CIRCUIT)

while True:
    led.toggle()
    crossing.next_tick()
    time.sleep(1)
