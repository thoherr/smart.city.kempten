# setup.py in root directory
# This is the configuration file to define the role of the raspi

from smart_city.controller_inner_city import ControllerInnerCity as SmartCityController

controller = SmartCityController(debug=True)
