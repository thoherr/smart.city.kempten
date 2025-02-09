# This is the second Raspi of our MOC of the City of Kempten
# It implements the second controller at Innenstadt, around the Rathaus, with traffic counts
# and two traffic lights

from machine import Pin

from domain.traffic.count import TrafficCount
from domain.traffic.light.column import Column as TrafficLightColumn
from domain.traffic.light.crossing import Crossing as TrafficLightCrossing
from report.traffic_count_panel import TrafficCountPanel
from smart_city.controller_base import ControllerBase


class ControllerInnerCityTwo(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._location = "Innenstadt"

        l1 = TrafficLightColumn(9, 10, 11, 1)
        l2 = TrafficLightColumn(14, 13, 12, 0)

        self.actors.append(TrafficLightCrossing("Rathausplatz", [l1, l2]))

        l3 = TrafficLightColumn(17, 18, 19, 1)
        l4 = TrafficLightColumn(22, 21, 20, 0)

        self.actors.append(TrafficLightCrossing("Gerberstrasse", [l3, l4]))

        in_traffic_1 = TrafficCount("RH 1 einwärts", Pin(27, Pin.IN), verbose=True)
        self.actors.append(in_traffic_1)
        out_traffic_1 = TrafficCount("RH 1 auswärts", Pin(26, Pin.IN), verbose=True)
        self.actors.append(out_traffic_1)

        counters_1 = [out_traffic_1, in_traffic_1]
        traffic_count_panel = TrafficCountPanel("traffic", self.i2c0, counters_1, verbose=True)
        self.actors.append(traffic_count_panel)

        in_traffic_2 = TrafficCount("RH 2 einwärts", Pin(4, Pin.IN), verbose=True)
        self.actors.append(in_traffic_2)
        out_traffic_2 = TrafficCount("RH 2 auswärts", Pin(5, Pin.IN), verbose=True)
        self.actors.append(out_traffic_2)

        in_traffic_3 = TrafficCount("RH 3 einwärts", Pin(6, Pin.IN), verbose=True)
        self.actors.append(in_traffic_3)
        out_traffic_3 = TrafficCount("RH 3 auswärts", Pin(7, Pin.IN), verbose=True)
        self.actors.append(out_traffic_3)

