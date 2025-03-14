# setup.py in root directory
# This is the configuration file to define the role of the raspi
# by defining the specific instance of a SmartCityController

# The file setup_values.py should contain the number of our controller/board, e.g.
#
#   # This specifies on which controller (PICO board) we are running
#   controller_number = 1
#
import setup_values

if setup_values.controller_number == 1:
    from smart_city.controller_inner_city_one import ControllerInnerCityOne as SmartCityController
elif setup_values.controller_number == 2:
    from smart_city.controller_inner_city_two import ControllerInnerCityTwo as SmartCityController
elif setup_values.controller_number == 3:
    from smart_city.controller_iller import ControllerIller as SmartCityController
else:
    raise ValueError('controller_number must be 1, 2 or 3')

controller = SmartCityController(number=setup_values.controller_number, debug=setup_values.debug)
