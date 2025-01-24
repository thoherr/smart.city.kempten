# This is the second Raspi of our MOC of the City of Kempten
# It implements the second controller at Innenstadt, around the Rathaus, with traffic counts
# and two traffic lights

import asyncio

from smart_city.controller_base import ControllerBase
from domain.traffic.light.column import Column as TrafficLightColumn
from domain.traffic.light.crossing import Crossing as TrafficLightCrossing
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper


class ControllerInnerCityTwo(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Innenstadt"

        self.actors = []

        self.actors.append(Heartbeat(verbose=True))
        self.actors.append(Housekeeper(verbose=False))

        l1 = TrafficLightColumn(9, 10, 11, 1)
        l2 = TrafficLightColumn(14, 13, 12, 0)

        self.actors.append(TrafficLightCrossing("Rathausplatz", [l1, l2]))

        l3 = TrafficLightColumn(17, 18, 19, 1)
        l4 = TrafficLightColumn(22, 21, 20, 0)

        self.actors.append(TrafficLightCrossing("Gerberstrasse", [l3, l4]))


    def print_debug_log(self):
        pass

    async def create_tasks(self):
        print("create_tasks()")
        tasks = []
        for actor in self.actors:
            tasks.append(asyncio.create_task(actor.run()))
