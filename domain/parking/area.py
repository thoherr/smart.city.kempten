# Parking area, consisting of a number of parking spaces
import asyncio

from domain.parking.space import ParkingSpace


class ParkingArea:
    def __init__(self, location : str, spaces : [ParkingSpace]):
        self.spaces = spaces
        self.location = location

    async def run(self):
        tasks = [asyncio.create_task(space.run()) for space in self.spaces]
        await asyncio.gather(*tasks)

    def number_of_spaces(self) -> int:
        return len(self.spaces)

    def number_of_empty_spaces(self) -> int:
        return len([s for s in self.spaces if s.empty()])
