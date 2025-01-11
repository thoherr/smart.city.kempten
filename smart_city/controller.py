import asyncio

from smart_city.controller_one import ControllerOne


class SmartCityController(ControllerOne):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug

    async def run_forever(self):
        while True:
            if self.debug:
                self.print_debug_log()
            await asyncio.sleep(5)
