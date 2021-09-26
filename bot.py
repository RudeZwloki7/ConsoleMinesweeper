import random


class Bot:
    def __init__(self):
        self.field = None
        # self.x = 0
        # self.y = 0
        self.first_move = True
        self.flags = None

    def __handle_reader(self, size, field):
        my_field = [[{'probability': -1., 'visible': False} for x in range(size)] for y in range(size)]
        hidden = 0
        for row in range(size):
            for col in range(size):
                if not field[row][col]['visible']:
                    hidden += 1
                else:
                    my_field[row][col]['visible'] = True

                if field[row][col]['visible'] and isinstance(field[row][col]['repr'], int):
                    hidden_nh = []
                    neighbours = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                                  (row, col - 1), (row, col + 1),
                                  (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
                    counter = 0
                    for cell in neighbours:
                        if 0 <= cell[0] < size and 0 <= cell[1] < size:
                            if field[cell[0]][cell[1]]['repr'] == 'F':
                                counter += 1

                            if not field[cell[0]][cell[1]]['visible']:
                                hidden_nh.append(cell)

                    for cell in hidden_nh:
                        if counter == field[row][col]['repr']:
                            probability = .0
                            my_field[cell[0]][cell[1]]['probability'] = probability
                        else:
                            probability = field[row][col]['repr'] / len(hidden_nh)
                            if my_field[cell[0]][cell[1]]['probability'] < probability or my_field[cell[0]][cell[1]][
                                'probability'] == -1.:
                                my_field[cell[0]][cell[1]]['probability'] = probability

        for row in range(size):
            for col in range(size):
                if not field[row][col]['visible']:
                    probability = self.flags / hidden
                    if my_field[row][col]['probability'] == -1.:
                        my_field[row][col]['probability'] = probability

        return my_field

    def read_field(self, field, flags):
        size = len(field)
        self.flags = flags
        my_field = self.__handle_reader(size, field)

        rev_field = [i[::-1] for i in field[::-1]]

        rev_my_field = self.__handle_reader(size, rev_field)

        for row in range(size):
            for col in range(size):
                if not field[row][col]['visible']:
                    probability = my_field[row][col]['probability'] * rev_my_field[size - row - 1][size - col - 1][
                        'probability']
                    my_field[row][col]['probability'] = probability

        self.field = my_field

    def move(self):
        size = len(self.field)
        x = 0
        y = 0
        action = 'Open'

        if self.first_move:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            self.field[x][y]['visible'] = True
            # return self.x + 1, self.y + 1, action
            self.first_move = False
            return x + 1, y + 1, action
        else:
            prob = 1.
            for row in range(size):
                for col in range(size):
                    if self.field[row][col]['probability'] >= 1.:
                        return row + 1, col + 1, 'Flag'

                    if not self.field[row][col]['visible'] and self.field[row][col]['probability'] < prob:
                        prob = self.field[row][col]['probability']
                        x = row
                        y = col

            return x + 1, y + 1, action
