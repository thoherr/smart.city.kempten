# smart.city.kempten - microcontrollers

The model contains three microcontrollers with different functionality, sensors and actors:

* [Inner City One](../smart_city/controller_inner_city_one.py)
  * 8 space parking area with display
  * smart waste at town hall (also shown on parking display)
  * MQTT upload of parking and smart waste data
  * wiring documented in [wiring_inner_city_1.pdf](wiring_inner_city_1.pdf)
  * hardware used
    * Raspberry Pico W
    * 3 multiplexers TCA9548A (two for parking spaces and one for waste containers)
    * 8 ToF sensors VL53L0X for parking spaces (via two multiplexers)
    * 3 light sensors GY302 / BH1750 for waste containers (via multiplexer)
    * 3 5mm LEDs for light barrier of waste containers
    * OLED display SH1106 for parking area and smart waste

* [Inner City Two](../smart_city/controller_inner_city_two.py)
  * 4 way traffic light at city hall, with traffic count and traffic count display for incoming street
  * MQTT upload of traffic count (6 sensors at main crossing)
  * 3 way traffic light
  * illuminated controller below street
  * wiring documented in [wiring_inner_city_2.pdf](wiring_inner_city_2.pdf)
  * hardware used
    * Raspberry Pico W
    * 7 traffic light columns with 3 0805 SMD LEDs (red/yellow/green) each, mounted behind trans red/yellow/green 1*1 round LEGO plates
    * 6 magnetic hall sensors KY-024 for traffic count at main crossing
    * 3 5mm LEDs for illumination of controller (below street)
    * OLED display SH1106 for traffic count of street entering the model at the left side

* [Iller](../smart_city/controller_iller.py)
  * 6 space parking area with display,
  * smart waste (also shown on parking display)
  * 4 way traffic crossing with traffic count and traffic count display for incoming street
  * environment sensor with display
  * MQTT upload of parking area, traffic count and environment data
  * wiring documented in [wiring_iller.pdf](wiring_iller.pdf)
  * hardware used
    * Raspberry Pico 2 W
    * 4 traffic light columns with 3 0805 SMD LEDs (red/yellow/green) each, mounted behind trans red/yellow/green 1*1 round LEGO plates
    * 3 multiplexers TCA9548A (one for parking spaces, one for waste containers and one for displays)
    * 6 ToF sensors VL53L0X for parking spaces (via multiplexer)
    * 3 light sensors GY302 / BH1750 for waste containers (via multiplexer)
    * 3 5mm LED for light barrier of waste containers
    * 6 magnetic hall sensors KY-024 for traffic count at main crossing
    * 3 OLED displays SH1106 for traffic count, parking area/smart waste and environmental data (via multiplexer)
