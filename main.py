from player import Player
from soldier import Soldier
from utilities import print_board

class LittleBattle:
    def __init__(self, gamelog_path):
        self.max_turn = 40
        self.open_gamelog_file(gamelog_path)
        self.players = []
        self.players.append(Player(1, self.resources, self.homeBase1))
        self.players.append(Player(2, self.resources, self.homeBase2))

        # # Starting message
        # print('Little Battle Game을 시작합니다.')
        # print('최대 플레이 가능한 턴은 35턴입니다.')
        # print('')

        # # print_board(self.board)
        # print_board(self.board)

    def __call__(self):
        turn = 0
        while True:
            if turn == self.max_turn:
                self.gameOver("Max turn reached.")
            else:
                return_Value = self.players[turn%2].__call__(self.board, self.players[int(not turn%2)].my_soldier,self.players[int(not turn%2)])
                if "invaded" in return_Value:
                    self.gameOver(return_Value)
                turn += 1

    def open_gamelog_file(self, file_path):
        with open(file_path, 'r') as f:
            data = f.readlines()
        self.width, self.height = map(int,data[0].split())

        # player 1,2 homebase (y,x)
        self.homeBase1 = tuple(map(int, data[1].split()))
        self.homeBase2 = tuple(map(int, data[2].split()))

        # resource (food, gold, wood)
        self.resources = tuple(map(int, data[3].split()))
        
        # max turn
        self.maxTurn = data[4]

        # board with tile info # 계속 북마크

        self.board = {}
        for y in range(self.height):
            self.board[y]={}
            tile_info = list(map(str, data[y+5].split()))
            for x in range(self.width):
                self.board[y][x]={}
                self.board[y][x]['tile'] = tile_info[x]

        # board with resource info & combine
        for y in range(self.height):
            resource_info = list(map(str, data[y+9].split()))
            for x in range(self.width):
                self.board[y][x]['resource'] = resource_info[x]
        # self.board_Resource = []

        # set home base
        for y in range(self.height):
            for x in range(self.width):
                if (y,x) == self.homeBase1:
                    self.board[y][x]['locate'] = 'P1'
                elif (y,x) == self.homeBase2:
                    self.board[y][x]['locate'] = 'P2'
                else:
                    self.board[y][x]['locate'] = 'N/A'
        # hb1_y, hb1_x = self.homeBase1
        # self.board[hb1_y][hb1_x] = 'H1'
        # hb2_y, hb2_x = self.homeBase2
        # self.board[hb2_y][hb2_x] = 'H2'
    
    def gameOver(self, message):
        score1 = self.players[0].score
        score2 = self.players[1].score
        if "invaded" in message:
            print(message)
        else:
            print("Player1's score: {}".format(score1))
            print("Player2's score: {}".format(score2))
        if score1 == score2:
            print("Tie!")
            exit()
        elif score1 > score2:
                winner = "Player1"
        else:
            winner = "Player2"
        print("{} won!".format(winner))
        exit()

    def print_debugg(self):
        print("debugging....")
        for key1, val1 in self.board.items():
            print(key1)
            for key2, val2 in val1.items():
                print(key2, end=' ** ')
                print(val2)
        # for row in range(self.height):
        #     for col in range(self.width):
        #         print('|', end = '')
        #         print(self.board[row][col])


# if __name__ == '__main__':
#     game = LittleBattle('./game_log1.txt')
#     game() 

# TODO

# 1. 보드 출력
# 2. console print (완성본) // 범위 내 숫자 입력하면 오류 메시지