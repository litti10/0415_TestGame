# f = open('text.txt', 'w')
# f.write("HelloWorld")
# f.close()

# file = open('text.txt', 'r')
# print(file.read())

# self.resources = {
#           'gold': resources[0],
#           'food': resources[1],
#           'wood': resources[2],
#         }
# tuple(self.resources.values)


# dic = {
#     'a': {
#         '1':{
#             'resource': 'sdaf',
#             'tile': 'adf'
#         }
#     },
#     'b': {
#         '0':{
#             'resource': 'ds',
#             'tile': 'aa'
#         }
#     }
# }

# for key1, val1 in dic.items():
#     print ('val1: ', end='')
#     print(val1)
#     for key2, val2 in val1.items():
#         print ('val2: ', end='')
#         print(val2)


# class bcolors:
#     BLUE = '\033[94m'
#     RED = '\033[91m'
#     BLACK = '\033[0m'
#     UNDERLINE = '\033[4m'


# board = [] 
# for h in range(4):
#     tmp = ['0 '] * 8
#     board.append(tmp)

# p1_soliders = [(1,1), (3,2)]
# p2_soliders = [(3,0), (6,1)]

# for y in range(4):
#     for x in range(8):
#         if (x,y) in p1_soliders:
#             color = bcolors.BLUE
#         elif (x,y) in p2_soliders:
#             color = bcolors.RED
#         else:
#             color = bcolors.BLACK
#         print('{}{}{}'.format(color, board[y][x], bcolors.BLACK), end='')
#     print('')

my_soldier = []

my_soldier.append({
            'location': (2,3),
            'type': 'A'
        })

my_soldier.append({
            'location': (3,3),
            'type': 'B'
        })

for items in my_soldier:
    print(items)