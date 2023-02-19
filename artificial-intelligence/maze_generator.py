import random

class Field:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        # generate field
        self.field = [['#' for _ in range(self.columns)] for _ in range(self.rows)]
        self.field[0][0] = 'S'
        # generate goal position
        self.field[random.randint(0, rows - 1)][random.randint(0, columns - 1)] = 'E'

    # generate maze

    def __str__(self):
        string = '\n'.join([' '.join(row) for row in self.field])
        return string

field = Field(20, 25)
print(field)