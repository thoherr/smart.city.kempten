import micropython

micropython.alloc_emergency_exception_buf(100)

from machine import Pin
import time

from traffic_light.column import Column as TrafficLightColumn
from traffic_light.crossing import Crossing as TrafficLightCrossing

led = Pin("LED", Pin.OUT)

l1 = TrafficLightColumn(18, 19, 20, 1)
l2 = TrafficLightColumn(13, 12, 11, 0)

states = [(1, [TrafficLightColumn.STOP, TrafficLightColumn.STOP]),
          (2, [TrafficLightColumn.PREPARE, TrafficLightColumn.STOP]),
          (5, [TrafficLightColumn.GO, TrafficLightColumn.STOP]),
          (1, [TrafficLightColumn.CAUTION, TrafficLightColumn.STOP]),
          (1, [TrafficLightColumn.STOP, TrafficLightColumn.STOP]),
          (2, [TrafficLightColumn.STOP, TrafficLightColumn.PREPARE]),
          (5, [TrafficLightColumn.STOP, TrafficLightColumn.GO]),
          (1, [TrafficLightColumn.STOP, TrafficLightColumn.CAUTION])]

crossing = TrafficLightCrossing([l1, l2], states)

while True:
    led.toggle()
    crossing.next_tick()
    time.sleep(1)
