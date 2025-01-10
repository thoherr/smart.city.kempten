import machine
from micropython import const

class Column:

    OFF = const(0)
    STOP = const(1)
    PREPARE = const(2)
    GO = const(3)
    CAUTION = const(4)

    def __init__(self, red_gpio, yellow_gpio, green_gpio, direction):
        self.red = machine.Pin(red_gpio, machine.Pin.OUT, value=0)
        self.yellow = machine.Pin(yellow_gpio, machine.Pin.OUT, value=0)
        self.green = machine.Pin(green_gpio, machine.Pin.OUT, value=0)
        self.direction = direction

    def change_to(self, state):
        if state == self.OFF:
            self.off()
        if state == self.STOP:
            self.stop()
        if state == self.PREPARE:
            self.prepare()
        if state == self.GO:
            self.go()
        if state == self.CAUTION:
            self.caution()

    def off(self):
        self.red.off()
        self.yellow.off()
        self.green.off()

    def stop(self):
        self.red.on()
        self.yellow.off()
        self.green.off()

    def prepare(self):
        self.red.on()
        self.yellow.on()
        self.green.off()

    def go(self):
        self.red.off()
        self.yellow.off()
        self.green.on()

    def caution(self):
        self.red.off()
        self.yellow.on()
        self.green.off()

