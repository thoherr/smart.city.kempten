from traffic_light.column import Column as Column

class Crossing:
    DEFAULT_CIRCUIT = ((1, (Column.STOP, Column.STOP)),
                       (2, (Column.PREPARE, Column.STOP)),
                       (10, (Column.GO, Column.STOP)),
                       (2, (Column.CAUTION, Column.STOP)),
                       (1, (Column.STOP, Column.STOP)),
                       (2, (Column.STOP, Column.PREPARE)),
                       (10, (Column.STOP, Column.GO)),
                       (2, (Column.STOP, Column.CAUTION)))

    OUT_OF_ORDER_CIRCUIT = ((1, (Column.CAUTION, Column.CAUTION)),
                            (1, (Column.OFF, Column.OFF)))

    def __init__(self, light_columns, circuit, initial_delay=2):
        self.light_columns = light_columns
        self.circuit = circuit
        self.current_index = 0
        self.delay = initial_delay + 1
        self.update_light_columns()

    def next_tick(self):
        self.delay -= 1
        if self.delay <= 0:
            self.current_index = (self.current_index + 1) % len(self.circuit)
            self.delay = self.circuit[self.current_index][0]
            self.update_light_columns()

    def update_light_columns(self):
        for light_column in self.light_columns:
            light_column.change_to(self.circuit[self.current_index][1][light_column.direction])
