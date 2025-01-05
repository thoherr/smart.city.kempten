from traffic_light.column import Column as Column

class Crossing:
    # circuit specification format:
    # this is a list of tuples containing the number of ticks for each phase
    # and a list of column status in this phase
    # the order in the status list is tha same as in the column list, the status
    # list has to have at least the number of columns entries
    # for efficiency the lists are also tuples
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

    def __init__(self, light_columns, default_circuit=DEFAULT_CIRCUIT, initial_delay=2):
        self.circuit = None
        self.current_index : int = None
        self.delay : int = None
        self.light_columns = light_columns
        self.default_circuit = default_circuit
        self.turn_on(default_circuit, initial_delay)

    def turn_on(self, circuit=None, initial_delay=None):
        self.current_index = 0
        self.circuit = circuit if circuit else self.default_circuit
        self.delay = initial_delay if initial_delay else self.circuit[self.current_index][0]
        self._update_light_columns()

    def turn_off(self):
        self.circuit = None
        for light_column in self.light_columns:
            light_column.change_to(Column.OFF)

    def next_tick(self):
        if not self.circuit:
            return
        self.delay -= 1
        if self.delay <= 0:
            self._next_phase()

    def _next_phase(self):
        self.current_index = (self.current_index + 1) % len(self.circuit)
        self.delay = self.circuit[self.current_index][0]
        self._update_light_columns()

    def _update_light_columns(self):
        for light_column in self.light_columns:
            light_column.change_to(self.circuit[self.current_index][1][light_column.direction])
