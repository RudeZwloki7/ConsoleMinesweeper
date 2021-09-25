def print_game_grid(field, flags):
    print('{:^{width}}'.format('MINESWEEPER', width=8*len(field)))

    print('{:>10} {}'.format('Flags:', flags), end='\n\n')

    print('\t', end='')
    for i in range(len(field)):
        print('{:^5}'.format(i+1), end='')
    print()

    print('\t', end=' ')
    for i in range(len(field)):
        print('{:_^5}'.format(''), end='')
    print()

    for row in range(len(field)):
        print(row+1, '|', sep='\t', end='')
        for col in range(len(field)):
            # if field[row][col]['visible']:
            #     print(field[row][col]['value'], end='')
            print('{:^4}|'.format(field[row][col]['repr'] if field[row][col]['visible'] else '#'), end='')

        print()
        print('\t', end=' ')
        for i in range(len(field)):
            print('{:_^5}'.format(''), end='')
        print()

    print()
