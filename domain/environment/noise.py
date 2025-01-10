class Noise:
    def __init__(self, location : str, analog_sensor):
        self.location = location
        self.analog_sensor = analog_sensor

    def noise(self):
        return self.analog_sensor.noise()
