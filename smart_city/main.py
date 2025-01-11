# main program for firmware app
# adapted from https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md#224-a-typical-firmware-app

import asyncio

from smart_city.controller import SmartCityController


def set_global_exception():
    def handle_exception(_self, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)


async def main():
    set_global_exception()
    controller = SmartCityController()
    tasks = controller.create_tasks()
    await asyncio.gather(tasks, controller.run_forever())


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()  # Clear retained state
