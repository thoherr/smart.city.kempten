
class Crossing:
    def __init__(self, light_columns, states, initial_delay = 2):
        self.light_columns = light_columns
        self.states = states
        self.state_index = 0
        self.delay = initial_delay + 1
        self.update_light_columns()

    def next_tick(self):
        self.delay -= 1
        if self.delay <= 0:
            self.state_index = (self.state_index + 1) % len(self.states)
            self.delay = self.states[self.state_index][0]
            self.update_light_columns()

    def update_light_columns(self):
        for light_column in self.light_columns:
            light_column.change_to(self.states[self.state_index][1][light_column.direction])
