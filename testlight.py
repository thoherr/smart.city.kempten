import micropython

micropython.alloc_emergency_exception_buf(100)

from machine import Pin
import time

from traffic_light.column import Column as TrafficLightColumn
from traffic_light.crossing import Crossing as TrafficLightCrossing

led = Pin("LED", Pin.OUT)

l1 = TrafficLightColumn(18, 19, 20, 1)
l2 = TrafficLightColumn(13, 12, 11, 0)

states = [[TrafficLightColumn.STOP, TrafficLightColumn.GO],
          [TrafficLightColumn.STOP, TrafficLightColumn.GO],
          [TrafficLightColumn.STOP, TrafficLightColumn.CAUTION],
          [TrafficLightColumn.STOP, TrafficLightColumn.STOP],
          [TrafficLightColumn.PREPARE, TrafficLightColumn.STOP],
          [TrafficLightColumn.GO, TrafficLightColumn.STOP],
          [TrafficLightColumn.GO, TrafficLightColumn.STOP],
          [TrafficLightColumn.CAUTION, TrafficLightColumn.STOP],
          [TrafficLightColumn.STOP, TrafficLightColumn.STOP],
          [TrafficLightColumn.STOP, TrafficLightColumn.PREPARE]]

crossing = TrafficLightCrossing([l1, l2], states)

while True:
    led.toggle()
    crossing.next_state()
    time.sleep(1)
