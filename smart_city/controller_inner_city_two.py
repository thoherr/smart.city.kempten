# This is the second Raspi of our MOC of the City of Kempten
# It implements the second controller at Innenstadt, around the Rathaus, with traffic counts
# and two traffic lights

from machine import Pin

from domain.traffic.count import TrafficCount
from domain.traffic.light.column import Column as TrafficLightColumn
from domain.traffic.light.crossing import Crossing as TrafficLightCrossing
from report.mqtt_upload import MqttUpload
from report.traffic_count_panel import TrafficCountPanel
from smart_city.controller_base import ControllerBase

from setup_values import *

class ControllerInnerCityTwo(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.debug:
            print("##### ControllerInnerCityTwo.__init__()")

        l1 = TrafficLightColumn(9, 10, 11, 1)
        l2 = TrafficLightColumn(14, 13, 12, 0)

        self.actors.append(TrafficLightCrossing("Rathausplatz", [l1, l2]))

        l3 = TrafficLightColumn(17, 18, 19, 1)
        l4 = TrafficLightColumn(22, 21, 20, 0)

        self.actors.append(TrafficLightCrossing("Gerberstrasse", [l3, l4], initial_delay=9))

        mqtt_traffic_1 = MqttUpload("verkehr/sck_verkehr_1", self.mqtt_client)

        in_traffic_1 = TrafficCount("RH 1 eingehend", "eingehend", Pin(27, Pin.IN), mqtt_traffic_1, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(in_traffic_1)
        out_traffic_1 = TrafficCount("RH 1 ausgehend", "ausgehend", Pin(26, Pin.IN), mqtt_traffic_1, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(out_traffic_1)

        counters_1 = [out_traffic_1, in_traffic_1]
        traffic_count_panel = TrafficCountPanel("traffic", self.i2c0, counters_1)
        self.actors.append(traffic_count_panel)

        mqtt_traffic_2 = MqttUpload("verkehr/sck_verkehr_2", self.mqtt_client)

        in_traffic_2 = TrafficCount("RH 2 eingehend", "eingehend", Pin(4, Pin.IN), mqtt_traffic_2, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(in_traffic_2)
        out_traffic_2 = TrafficCount("RH 2 ausgehend", "ausgehend", Pin(5, Pin.IN), mqtt_traffic_2, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(out_traffic_2)

        mqtt_traffic_3 = MqttUpload("verkehr/sck_verkehr_3", self.mqtt_client)

        in_traffic_3 = TrafficCount("RH 3 eingehend", "eingehend", Pin(6, Pin.IN), mqtt_traffic_3, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(in_traffic_3)
        out_traffic_3 = TrafficCount("RH 3 ausgehend", "ausgehend", Pin(7, Pin.IN), mqtt_traffic_3, interval=TRAFFIC_COUNT_CHECK_INTERVAL)
        self.actors.append(out_traffic_3)

