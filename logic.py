import random
from draw_field import print_game_grid


class Game:
    def __init__(self, mines, size):
        self.mines = mines
        self.size = size
        self.mines_cords = self.__generate_mines_pos(mines, size)
        self.flags_cords = []
        self.flags = mines
        self.gen_field = self.__generate_field()
        self.is_lose = False
        self.is_win = False

    def __generate_mines_pos(self, mines, size):
        mines_pos = []
        for i in range(mines):
            mine_cords = {'x': random.randint(0, size - 1), 'y': random.randint(0, size - 1)}
            while mine_cords in mines_pos:
                mine_cords = {'x': random.randint(0, size - 1), 'y': random.randint(0, size - 1)}
            mines_pos.append(mine_cords)

        return mines_pos

    def __count_mines(self, row, col):
        if (row, col) in [(x['x'], x['y']) for x in self.mines_cords]:
            return -1
        neighbours = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                      (row, col - 1), (row, col + 1),
                      (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
        counter = sum(el in neighbours for el in [(x['x'], x['y']) for x in self.mines_cords])

        return counter

    def __generate_field(self):
        field = [[{'value': 0, 'visible': False, 'with_flag': False,
                   'repr': ''} for x in range(self.size)] for y in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                cell = self.__count_mines(row, col)
                if cell == -1:
                    representation = 'M'
                elif cell == 0:
                    representation = ' '
                else:
                    representation = cell

                field[row][col].update({'value': cell, 'visible': False, 'with_flag': False, 'repr': representation})

        return field

    def __lose_game(self, field):
        for row in range(self.size):
            for col in range(self.size):
                if field[row][col]['with_flag'] and field[row][col]['value'] != -1:
                    field[row][col]['repr'] = 'X'

                field[row][col]['visible'] = True
        self.is_lose = True
        print_game_grid(field=field, flags=self.flags)

    def __win_game(self, field):
        for row in range(self.size):
            for col in range(self.size):
                field[row][col]['visible'] = True
        self.is_win = True
        print_game_grid(field=field, flags=self.flags)

    def __player_turn(self, player_x, player_y, flag, field):
        if flag == 'Flag':
            if not field[player_x][player_y]['with_flag'] and self.flags > 0 and not field[player_x][player_y]['visible']:
                field[player_x][player_y]['repr'] = 'F'
                field[player_x][player_y]['visible'] = True
                field[player_x][player_y]['with_flag'] = True
                self.flags -= 1
                self.flags_cords.append({'x': player_x, 'y': player_y})
                if self.flags_cords == self.mines_cords:
                    self.__win_game(field)

            elif field[player_x][player_y]['with_flag']:
                field[player_x][player_y]['repr'] = self.gen_field[player_x][player_y]['repr']
                field[player_x][player_y]['visible'] = False
                field[player_x][player_y]['with_flag'] = False
                self.flags += 1
                self.flags_cords.remove({'x': player_x, 'y': player_y})

        if flag == 'Open':
            if not field[player_x][player_y]['visible']:
                if field[player_x][player_y]['value'] == -1:
                    self.__lose_game(field)
                elif field[player_x][player_y]['value'] > 0:
                    if not field[player_x][player_y]['with_flag']:
                        field[player_x][player_y]['visible'] = True
                elif field[player_x][player_y]['value'] == 0:
                    vis_cells = []
                    self.__open_neighbours(field, player_x, player_y, vis_cells)

    def __open_neighbours(self, field, row, col, visited_cells):
        if [row, col] not in visited_cells:
            visited_cells.append([row, col])
            # If the cell is zero-valued
            if field[row][col]['value'] == 0:
                field[row][col]['repr'] = ' '
                if field[row][col]['with_flag']:
                    self.flags += 1
                    field[row][col]['with_flag'] = False
                field[row][col]['visible'] = True

                # Recursive calls for the neighbouring cells
                if row > 0:
                    self.__open_neighbours(field, row - 1, col, visited_cells)
                if row < self.size - 1:
                    self.__open_neighbours(field, row + 1, col, visited_cells)
                if col > 0:
                    self.__open_neighbours(field, row, col - 1, visited_cells)
                if col < self.size - 1:
                    self.__open_neighbours(field, row, col + 1, visited_cells)
                if row > 0 and col > 0:
                    self.__open_neighbours(field, row - 1, col - 1, visited_cells)
                if row > 0 and col < self.size - 1:
                    self.__open_neighbours(field, row - 1, col + 1, visited_cells)
                if row < self.size - 1 and col > 0:
                    self.__open_neighbours(field, row + 1, col - 1, visited_cells)
                if row < self.size - 1 and col < self.size - 1:
                    self.__open_neighbours(field, row + 1, col + 1, visited_cells)

                    # If the cell is not zero-valued
            if field[row][col]['value'] != 0:
                if field[row][col]['with_flag']:
                    self.flags += 1
                field[row][col]['visible'] = True

    def run(self):
        game_field = self.gen_field

        while not self.is_lose and not self.is_win:
            print_game_grid(field=game_field, flags=self.flags)
            print('Enter cords and action (Open or Flag) as X Y Action:', end='\t')
            player_input = input()
            player_x, player_y, flag = [val for val in player_input.split()]
            self.__player_turn(int(player_x) - 1, int(player_y) - 1, flag, game_field)

        if self.is_win:
            print('\n CONGRATULATIONS!!!\n You win!')
        else:
            print('\nYOU LOSE!!!')