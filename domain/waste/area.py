# Waste area, consisting of a number of waste containers
import asyncio

from domain.waste.container import WasteContainer


class WasteArea:
    def __init__(self, wa_id: str, containers: [WasteContainer]):
        self.id = wa_id
        self.containers = containers

    async def run(self):
        tasks = [asyncio.create_task(container.run()) for container in self.containers]
        await asyncio.gather(*tasks)

    def status(self):
        status = {}
        for i, container in enumerate(self.containers):
            status[f"tonne_{i + 1}"] = 1 if container.full() else 0
        return status
