class Sensor:
    def __init__(self, location):
        self.location = location

    def value(self):
        raise NotImplementedError("value() has to be implemented by child class")
