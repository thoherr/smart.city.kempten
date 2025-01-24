# setup.py in root directory
# This is the configuration file to define the role of the raspi
# by defining the specific instance of a SmartCityController

from smart_city.controller_inner_city_one import ControllerInnerCityOne as SmartCityController
#from smart_city.controller_inner_city_two import ControllerInnerCityTwo as SmartCityController
#from smart_city.controller_iller import ControllerIller as SmartCityController

controller = SmartCityController(debug=True)
