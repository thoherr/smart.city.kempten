# This is the second Raspi of our MOC of the City of Kempten
# It implements the second controller at Innenstadt, around the Rathaus, with traffic counts
# and two traffic lights

import asyncio

from smart_city.controller_base import ControllerBase
from util.heartbeat import Heartbeat
from util.housekeeper import Housekeeper


class ControllerInnerCityTwo(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Innenstadt"

        self.actors = []

        self.actors.append(Heartbeat(verbose=True))
        self.actors.append(Housekeeper(verbose=False))

        # TODO: Add Actors


    def print_debug_log(self):
        pass

    async def create_tasks(self):
        print("create_tasks()")
        tasks = []
        for actor in self.actors:
            tasks.append(asyncio.create_task(actor.run()))
