
class Crossing:
    def __init__(self, light_columns, states):
        self.light_columns = light_columns
        self.states = states
        self.state_index = 0
        self.tick = 0
        self.update_light_columns()

    def next_tick(self):
        self.tick += 1
        if self.tick >= self.states[self.state_index][0]:
            self.tick = 0
            self.state_index = (self.state_index + 1) % len(self.states)
            self.update_light_columns()

    def update_light_columns(self):
        for light_column in self.light_columns:
            light_column.change_to(self.states[self.state_index][1][light_column.direction])
