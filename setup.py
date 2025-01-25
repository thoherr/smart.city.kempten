# setup.py in root directory
# This is the configuration file to define the role of the raspi
# by defining the specific instance of a SmartCityController

# the file setup_controller_number.py should contain the number of our controller/board, e.g.
# controller_number = 1
import setup_controller_number

if setup_controller_number.controller_number == 1:
    from smart_city.controller_inner_city_one import ControllerInnerCityOne as SmartCityController
elif setup_controller_number.controller_number == 2:
    from smart_city.controller_inner_city_two import ControllerInnerCityTwo as SmartCityController
elif setup_controller_number.controller_number == 3:
    from smart_city.controller_iller import ControllerIller as SmartCityController
else:
    raise ValueError('controller_number must be 1, 2 or 3')

controller = SmartCityController(debug=True)
