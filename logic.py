import random

from bot import Bot
from draw_field import print_game_grid
import os
import pandas as pd
import uuid

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


class Game:
    def __init__(self, mode, mines, size):
        self.mode = mode
        self.mines = mines
        self.size = size
        self.mines_cords = self.__generate_mines_pos(mines, size)
        self.flags_cords = []
        self.flags = mines
        self.gen_field = self.__generate_field()
        self.is_lose = False
        self.is_win = False
        self.save_dir = os.path.join(repo_root, '.saves')
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            os.chmod(self.save_dir, 777)

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
            if not field[player_x][player_y]['with_flag'] and self.flags > 0 and not field[player_x][player_y][
                'visible']:
                field[player_x][player_y]['repr'] = 'F'
                field[player_x][player_y]['visible'] = True
                field[player_x][player_y]['with_flag'] = True
                self.flags -= 1
                self.flags_cords.append({'x': player_x, 'y': player_y})

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

        if self.__compare(self.flags_cords, self.mines_cords):
            self.__win_game(field)

    def __compare(self, first, second):
        if len(first) == len(second):
            counter1 = 0
            counter2 = 0
            for el in first:
                if el in second:
                    counter1 += 1
                else:
                    return False

            for el in second:
                if el in first:
                    counter2 += 1
                else:
                    return False

            if counter1 == counter2 and counter1 == len(first):
                return True

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

    def __get_field_val(self):
        field = [[0 for x in range(self.size)] for y in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                field[row][col] = self.gen_field[row][col]['value']

        return field

    def run(self):
        game_field = self.gen_field
        is_bot = True if self.mode == '1' else False
        bot = Bot()

        while not self.is_lose and not self.is_win:
            print_game_grid(field=game_field, flags=self.flags)
            print('Enter cords and action (Open or Flag) as X Y Action:', end='\t')
            if is_bot:
                bot.read_field(game_field, self.flags)
                player_x, player_y, flag = bot.move()
                print(player_x, player_y, flag)
            else:
                player_input = input()
                player_x, player_y, flag = [val for val in player_input.split()]

            self.__player_turn(int(player_x) - 1, int(player_y) - 1, flag, game_field)

        if self.is_win:
            print('\n CONGRATULATIONS!!!\n You win!')
            from logger import filename
            file_path = os.path.join(self.save_dir, f'win_{filename}.csv')
            df = pd.DataFrame(data=self.__get_field_val())
            with open(file_path, 'w') as f:
                df.to_csv(file_path, sep=',', index=False)
                f.close()
        else:
            print('\nYOU LOSE!!!')
            from logger import filename
            file_path = os.path.join(self.save_dir, f'lose_{filename}.csv')
            df = pd.DataFrame(data=self.__get_field_val(), )
            with open(file_path, 'w') as f:
                df.to_csv(file_path, sep=',', index=False)
                f.close()
