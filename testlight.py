import asyncio

import micropython

micropython.alloc_emergency_exception_buf(100)

from machine import Pin

from domain.traffic.light.column import Column as TrafficLightColumn
from domain.traffic.light.crossing import Crossing as TrafficLightCrossing
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper

led = Pin("LED", Pin.OUT)

l1 = TrafficLightColumn(9, 10, 11, 1)
l2 = TrafficLightColumn(14, 13, 12, 0)

crossing = TrafficLightCrossing("Testcrossing", [l1, l2])


async def main_loop():
    print("----- main_loop starting")
    i = 0
    while True:
        if i == 65:
            crossing.turn_on(TrafficLightCrossing.OUT_OF_ORDER_CIRCUIT)
        elif i == 75:
            crossing.turn_off()
        if i == 85:
            crossing.turn_on(TrafficLightCrossing.OUT_OF_ORDER_CIRCUIT)
        elif i == 99:
            crossing.turn_on()
            i = 0


async def main():
    print("##### main starting")
    await asyncio.gather(asyncio.create_task(crossing.run()),
                         asyncio.create_task(Heartbeat(verbose=True).run()),
                         asyncio.create_task(Housekeeper(verbose=True).run()))


print("##### Testlight starting")
asyncio.run(main())
print("##### Testlight done")
