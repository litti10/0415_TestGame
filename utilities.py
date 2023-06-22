from color import bcolors
def print_board(board):
    tile_dict = {
        '0': 'Ground',
        '1': 'Poison',
        '2': 'Water '
    }
    resource_dict={
        '0': ' -- ',
        'G': 'Gold',
        'W': 'Wood',
        'F': 'Food'
    }
    soldier_dict = {
        'Scout': 'C',
        'Archer': 'A',
        'Spearman': 'S',
        'Knight': 'K'
    }
    color = bcolors.BLACK
    for key1, val1 in board.items():
            for key2, val2 in val1.items():
                tile_print = '|'
                tile_print += tile_dict[val2['tile']]
                tile_print += ' '
                tile_print += resource_dict[val2['resource']]
                tile_print += ' '
                print(tile_print, end='')
                if val2['locate'] != 'N/A':
                    if val2['locate'] == 'P1':
                        color = bcolors.BLUE
                        print('{}{}{}'.format(color, val2['locate'], bcolors.BLACK), end='')
                    elif val2['locate'] == 'P2':
                        color = bcolors.RED
                        print('{}{}{}'.format(color, val2['locate'], bcolors.BLACK), end='')
                    else:
                        if val2['locate'][-1] == '1':
                            color = bcolors.BLUE
                            
                            print('{}{}{}'.format(color, soldier_dict[val2['locate'][:-1]]+' ', bcolors.BLACK), end='')
                        else:
                            color = bcolors.RED
                            print('{}{}{}'.format(color, soldier_dict[val2['locate'][:-1]]+' ', bcolors.BLACK), end='')
                else:
                    tile_print += '  '
                    print('{}{}{}'.format(color, '  ', bcolors.BLACK), end='')
                print('|', end=' ')
            print()
                     

    # for row in 
    # print('---------------------------------------')
    # for row in board:
    #     for col in board[row]:
    #         board='|'
    #         if col
    #     print('')
    #     print('---------------------------------------')


"""
# board with tile info
self.board = []
for row in range(5,9):
    self.board.append(list(map(str, data[row].split())))

# board with resource info & combine
self.board_Resource = []
for row in range(9,13):
    self.board_Resource.append(list(map(str, data[row].split())))

# board with resource info & combine
    self.board_Resource = []
    for row in range(9,13):
        self.board_Resource.append(list(map(str, data[row].split())))

    for row in range(self.height):
        for col in range(self.width):
            if self.board_Resource[row][col] != '0':
                self.board[row][col] += self.board_Resource[row][col]
            else:
                self.board[row][col] += ' ' 


0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0

0 0 0 0 0 0 G 0
0 0 0 0 G 0 0 0
0 0 W 0 0 F 0 0
0 0 0 0 0 0 0 0
"""