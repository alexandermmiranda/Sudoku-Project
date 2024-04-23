import itertools
class Board:
    def __init__(self):
        self.fields = []
        self.rows = {i: [] for i in range(9)}
        self.columns = {i: [] for i in range(9)}
        self.blocks = {i: [] for i in range(9)}
        self.filled = 0
        for i, pos in enumerate(itertools.product(range(9), range(9))):
            #replace cell if the class for cell is different#
            self.fields.append(cell(*pos))
            self.rows[pos[0]].append(self.fields[i])
            self.columns[pos[1]].append(self.fields[i])
            self.blocks[self.fields[i].block].append(self.fields[i])

    def check_possible(self, field):
        if field.value != 0:
            return 0
        forbidden_values = set([])
        units = [self.rows[field.row], self.columns[field.column], self.blocks[field.block]]
        for unit in units:
            for unit_element in unit:
                forbidden_values.add(unit_element.value)
        field.permitted_values = set([i + 1 for i in range(9)]) - forbidden_values

    def load_game(self, fields):
        for i, j in enumerate(fields):
            self.fields[i].value = j
            if j != 0:
                self.filled += 1

    def export_game(self):
        return [self.fields[i].value for i in range(81)]

    def print_board(self):
        for i in range(9):
            print(*self.rows[i])

    def solve(self):
        while self.filled < 81:
            for field in self.fields:
                self.check_possible(field)
                if len(field.permitted_values) == 1:
                    field.value = list(field.permitted_values)[0]
                    self.filled += 1
        print("Board solved!")
        self.print_board()
