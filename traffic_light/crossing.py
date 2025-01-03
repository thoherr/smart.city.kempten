
class Crossing:
    def __init__(self, light_columns, states):
        self.light_columns = light_columns
        self.states = states
        self.state_index = 0

    def next_state(self):
        self.state_index = (self.state_index + 1) % len(self.states)
        for light_column in self.light_columns:
            light_column.change_to(self.states[self.state_index][light_column.direction])
