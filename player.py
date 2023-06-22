from utilities import print_board
from soldier import Soldier

class Player:
    def __init__(self, pid, resources, homebase):
        self.pid = pid 
        self.resources = {
          'gold': resources[0],
          'food': resources[1],
          'wood': resources[2],
        }
        self.my_soldier = []
        self.hire_remaining = 2
        self.cost_dict = Soldier.get_cost_dict()
        self.soldier_list = list(self.cost_dict.keys())
        self.homebase = homebase
        self.score = 0

    def __call__(self, board, enemy_list, EnemyPlayer):
        self.board = board
        print('Player'+str(self.pid)+'의 차례입니다.')
        print('')
        print_board(board)
        print('')
        possible_command = ['1','2','3','4']
        while True:
            command = self.print_commandBox()
            if command == 'end':
                exit()
            if not command in possible_command:
                print('unvalid command')
            elif command == '1':
                self.print_CurrResources()
                print('')
                self.print_SoliderPrice()
                print('')
                self.hire_Solider(enemy_list, EnemyPlayer)
                print('')
            
            elif command == '2':
                return_value = self.move_Soldier(enemy_list, EnemyPlayer)
                if "invaded" in return_value:
                    return return_value
            elif command == '3':
                print_board(board)
            elif command == '4':
                print('next turn')
                break
        
        self.reset_params()
        return '0'
       
    def reset_params(self):
        self.hire_remaining = 2
        for elem in self.my_soldier:
            elem.movable = True
        
    def print_CurrResources(self):
        message = '현재 당신의 자원: '
        for k,v in self.resources.items():
            message += "{}({})  ".format(k,v)
        print(message)
        
    def print_SoliderPrice(self):
        print('용병의 가격:')
        message = ''
        for elem in self.soldier_list:
            if elem != 'Spearman':
                message += elem+'\t:  '
            else:
                message += elem+':  '
            for key, value in self.cost_dict[elem].items():
                message += "{}({})  ".format(key,value)
            message += '\n'
        print(message)
    
    def hire_Solider(self, enemy_list, EnemyPlayer):
        if self.hire_remaining <= 0:
            print('잔여 횟수가 부족합니다.')
        else:
            print('어떤 용병을 구입하시겠습니까 ? (잔여: '+str(self.hire_remaining)+')')
            
            idx = 0
            for elem in self.soldier_list:
                print("{}. {}".format(idx+1,self.soldier_list[idx]), end = ' ')
                idx += 1
            print("{}. Return".format(idx+1))

            command_dict = {
                '1': 'Archer',
                '2': 'Spearman',
                '3': 'Knight',
                '4': 'Scout',
                '5': 'Return'
            }

            command = input()
            if not command in command_dict:
                print('unvalid input')
            elif command == '5':
                return
            else:
                request_s_type = command_dict[command]
                request_s_cost = self.cost_dict[request_s_type]

                message=''
                for key in request_s_cost:
                    temp_resource = self.resources[key] - request_s_cost[key]
                    if temp_resource < 0:
                        message =+ "{}가 {}만큼 부족합니다. \n".format(key,abs(temp_resource))
                
                if message == '': # 고용 성공
                    while True:
                        FLAG = self._locate_Solider(request_s_type, enemy_list, EnemyPlayer)
                        if FLAG == 'cancel':
                            break
                        elif FLAG:
                            for key in request_s_cost:
                                self.resources[key] = self.resources[key] - request_s_cost[key]
                            message ="{}을/를 고용했습니다.".format(request_s_type)
                            print(message)
                            self.hire_remaining -= 1
                            print("잔여 횟수: "+str(self.hire_remaining))
                            self.print_CurrResources()
                            break
                        else: 
                            before_message = "{}을/를 고용하지 못했습니다.".format(request_s_type)
                            print(before_message)
                            print(message)
                        
                    
                else: # 고용 실패
                    before_message = "{}을/를 고용하지 못했습니다.".format(request_s_type)
                    print(before_message)
                    print(message)
            
    def _locate_Solider(self, request_s_type, enemy_list, EnemyPlayer):
        print_board(self.board)
        print("")
        print("용병을 배치할 좌표를 입력해주세요. 만약 배치를 취소하시고 싶으신 경우, cancel을 입력하세요.")
        print("x y: ", end = '')
        user_input = list(input().split())

        if 'cancel' in user_input:
            return 'cancel'
        
        # error checking
        message = self.xy_exemption(user_input, '',request_s_type, 'locate')
        if message != 'success':
            message = "Unvalid input: " + message
            print (message)
            return False
        else:
            x = int(user_input[0])
            y = int(user_input[1])
                    
            self.my_soldier.append(Soldier(x,y, request_s_type))
            self.board[y][x]['locate'] = request_s_type + str(self.pid)
            print("병사가 배치되었습니다.")

            message = self.tile_eventcheck((y,x), enemy_list, EnemyPlayer, -1)
            if message != "success":
                message = "배치된 병사가 해당 사유로 사망했습니다: " + message
                print(message)
            
            print_board(self.board)
            return True

    def move_Soldier(self, enemy_list, EnemyPlayer):
       user_input_idx = self._select_Soldier()
       if user_input_idx == 'fail':
           return '0'
       
       init_loc_x = self.my_soldier[user_input_idx].x
       init_loc_y = self.my_soldier[user_input_idx].y
       while True:
            print_board(self.board)
            print("{}({},{})를 선택하셨습니다. 옮길 위치를 지정해주세요. 만약 옮기기를 취소하실 경우, cancel을 입력해주세요.".format(self.my_soldier[user_input_idx].type,self.my_soldier[user_input_idx].x,self.my_soldier[user_input_idx].y))
            print("x y: ", end = '')

            user_input = list(input().split())
            if 'cancel' in user_input:
                return '0'
            
            # error checking
            message = self.xy_exemption(user_input, (init_loc_y,init_loc_x), self.my_soldier[user_input_idx].type, 'move')
            if message != 'success':
                message = "Unvalid input: " + message
                print (message)
            else:
                x = int(user_input[0])
                y = int(user_input[1])
                
                final_loc = self._move_Soldier_stepbystep((init_loc_y,init_loc_x),(y,x), enemy_list, EnemyPlayer, user_input_idx)
                if final_loc == (-1,-1):
                    print("이동에 성공했습니다.")
                    self.my_soldier[user_input_idx].x = x
                    self.my_soldier[user_input_idx].y = y
                    self.board[y][x]['locate'] = self.my_soldier[user_input_idx].type + str(self.pid)
                    self.my_soldier[user_input_idx].movable = False
                    self.board[init_loc_y][init_loc_x]['locate'] = 'N/A'
                else:
                    if "invaded" in final_loc:
                        return final_loc
                    elif "사망" in final_loc:
                        self.board[init_loc_y][init_loc_x]['locate'] = 'N/A'
                    print(final_loc)

                print_board(self.board)
                return '0'
   
    def _select_Soldier(self):
        if len(self.my_soldier) == 0:
            print('현재 고용된 병사가 없습니다')
            return 'fail'
    
        while True:
            print("몇 번째 병사를 움직이시겠습니까? 움직이기를 취소하실 경우, cancel을 입력해주세요.")
            print("병사 리스트:")
            print('[타입] + [x,y 좌표]')
            movable_solNum = 0
            for i, soldier in enumerate(self.my_soldier):
                print("{}. {} ({},{})". format(str(i+1), soldier.type, str(soldier.x), str(soldier.y)), end = '')
                movable_solNum += 1
                if not soldier.movable:
                    print(" // 현재 이동불가", end = '')
                print('')
                
            user_input = list(input().split())

            if 'cancel' in user_input:
                return 'fail'
            
            message = self.singleValue_exemption(user_input, movable_solNum)
            # error checking
            if message != 'success':
                message = 'Unvalid Input: '+message
                print(message)
                print('')
            else:
                user_input_idx = int(user_input[0])-1
                if not self.my_soldier[user_input_idx].movable:
                    print("이번 턴에서 이미 이동한 적 있는 병사입니다.")
                else:
                    return user_input_idx
         
    def _move_Soldier_stepbystep(self, init_loc, destination_loc, enemy_list, EnemyPlayer, user_input_idx):
        init_loc_y, init_loc_x = init_loc
        y, x = destination_loc
        move_dir_List = [
            (0,1),
            (0,-1),
            (1,0),
            (-1,0)
        ]

        if init_loc_x == x:
            if init_loc_y < y:
                move_dir = move_dir_List[0]
            elif init_loc_y > y:
                move_dir = move_dir_List[1]
        elif init_loc_y == y:
            if init_loc_x < x:
                move_dir = move_dir_List[2]
            elif init_loc_x > x:
                move_dir = move_dir_List[3]

        cy = init_loc_y
        cx = init_loc_x
        while cx != x or cy != y:
            dx,dy = move_dir
            cy += dy
            cx += dx
            message = self.tile_eventcheck((cy, cx), enemy_list, EnemyPlayer, user_input_idx)
            if "invaded" in message:
                return message
            elif message != "success":
                message = '이동 중 해당 상황 발생: '+ message
                return message

        return (-1,-1)

    def fight_Soldier(self, location, my_sol_loc, enemy_list, EnemyPlayer):
        # 8 fight
        y,x = location
        my_sol = self.my_soldier[my_sol_loc]

        for enemy in enemy_list:
            if enemy.y == y and enemy.x == x:
                print("{}와 {}의 싸움이 시작됩니다".format(my_sol.type, enemy.type))
                if self.my_soldier[my_sol_loc].fight(my_sol.type, enemy.type) == 'win':
                    print("{}'s {} won!".format("Player"+str(self.pid), my_sol.type))
                    enemy_list.remove(enemy)
                    # 스코어 획득
                    self.add_Score(5)
                    return "win"
                elif self.my_soldier[my_sol_loc].fight(my_sol.type, enemy.type) == 'lose':
                    print("{}'s {} won!".format("Player"+str((self.pid)%2+1), enemy.type))
                    self.board[y][x]['locate'] = str(enemy.type)+str((self.pid)%2+1)
                    self.my_soldier.remove(self.my_soldier[my_sol_loc])
                    # 상대 스코어 획득
                    EnemyPlayer.add_Score(5)
                    
                    return "lose"
                elif self.my_soldier[my_sol_loc].fight(my_sol.type, enemy.type) == 'tie':
                    print("Tie!")
                    self.my_soldier.remove(self.my_soldier[my_sol_loc])
                    enemy_list.remove(enemy)
                    return "tie"
        return "N/A"

    def tile_eventcheck(self, location, enemy_list, EnemyPlayer, sol_num):
        y,x = location
        request_s_type = self.my_soldier[sol_num].type

        # resource check
        self._get_resource(location)

        # if poison - die
        if self.board[y][x]['tile'] == '1':
            self.my_soldier.remove(self.my_soldier[sol_num])
            return "독늪을 밟아서 {}이 사망했습니다.".format(request_s_type)
        
        # if water - cannot move
        if self.board[y][x]['tile'] == '2' and request_s_type != 'Scout':
            return "앞에 물이 있어 더 이상 이동할 수 없습니다."
        
        # if encounter enemy - fight
        result = self.fight_Soldier((y,x), sol_num, enemy_list, EnemyPlayer)

        if result == 'lose' or result == 'tie':
            return "적군과 전투 결과, {}이 사망했습니다.".format(request_s_type)
        
        # if homebase - cannot move
        if (self.pid == 1 and self.board[y][x]['locate'] == 'P1') or (self.pid == 2 and self.board[y][x]['locate'] == 'P2'):
            return "앞에 {}의 home base가 존재하여 지나갈 수 없습니다.".format('Player'+str(self.pid))
        
        if (self.pid == 1 and self.board[y][x]['locate'] == 'P2') or (self.pid == 2 and self.board[y][x]['locate'] == 'P1'):
            self.add_Score(99999999999)
            return "Player{}'s {} invaded Player{}'s homebase!".format(self.pid, request_s_type, str((self.pid%2)+1))
        
        return "success"
                    
    def _get_resource(self, location):
        y,x = location
        resource_dict = {
            'G':'gold',
            'W':'wood',
            'F':'food'
        }
        if self.board[y][x]['resource'] != '0':
            resource_type = resource_dict[self.board[y][x]['resource']]
            
            print("************")
            print("자원을 획득했습니다. 획득한 자원: {}".format(resource_type))
            print("************")
            self.resources[resource_type] += 1
            self.board[y][x]['resource'] = '0'
            # 스코어 획득
            self.add_Score(1)
        return

    def xy_exemption(self, user_input, init_location, request_s_type, check_loc):
        # error checking
        # 1 length check
        if len(user_input) != 2:
            return 'length error'

        # 2 format check
        for elem in user_input:
            if not elem.isnumeric():
                return 'format error'
        
        x = int(user_input[0])
        y = int(user_input[1])

        # 3 out of board
        if x < 0 or x >= len(self.board[0]) or y <0 or y >= len(self.board):
            return 'out of board'
        
        # 4 tile type?
        if self.board[y][x]['tile'] == '2' and request_s_type != 'Scout':
            return "{} cannot be located on the water tile".format(request_s_type)

        # 5 my solider already at the location
        for soldier in self.my_soldier:
            if x == soldier.x and y == soldier.y:
                return 'Other soldier is already located at the location.'
            
        # 6 homebase?
        if self.board[y][x]['locate'] == 'P'+str(self.pid):
            return 'You cannot locate solidiers at your homebase.'
        
        # 7 - 1 adjacent 8 block? // only for hiring
        if check_loc == 'locate':
            available_list = []
            move_command = [
                (1,0),
                (1,1),
                (0,1),
                (-1,1),
                (-1,0),
                (-1,-1),
                (0,-1),
                (1,-1)
            ]

            c_y, c_x = self.homebase
            for d_y, d_x in move_command:
                n_y = c_y + d_y
                n_x = c_x + d_x

                if n_x >= 0 and n_x < len(self.board[0]) and n_y >= 0 and n_y < len(self.board):
                    available_list.append((n_y, n_x))
                    available = True
                
            if (y,x) not in available_list:
                return 'You cannot locate solider out of the adjacent eight tile.'
        
        # 7 - 2 one direction moving // only for moving
        if check_loc == 'move':
            init_y, init_x = init_location
            if init_y - y != 0 and init_x-x != 0:
                return 'You can only move in one direction.'
        # 7 - 3 scout 2 tiles / others 1 tile movable
            elif (abs(init_y - y) > 1 or abs(init_x - x) >1) and request_s_type != 'Scout':
                return '{} can only move by maximum one tile.'.format(request_s_type)
            elif (abs(init_y - y) > 2 or abs(init_x - x) > 2) and request_s_type == 'Scout':
                return 'scout can only move by maximum two tile.'
        return 'success'

    def singleValue_exemption(self, user_input, movable_solNum):
        
        # 1 lenght error
        if len(user_input) != 1:
            return 'Enter one integer'
        
        user_input = user_input[0]

        # 2 format error
        if not user_input.isnumeric():
            return 'Not integer'
        
        user_input = int(user_input)

        if movable_solNum != '':
            # 3 range error
            if user_input > movable_solNum or user_input < 1:
                return 'Not in range'
        return 'success'
     
    def print_commandBox(self):
        command_List = [
            'Recruit Soldiers',
            'Move Soldiers',
            'Print Board',
            'Finish Turn'
            ]
        
        for idx in range (len(command_List)):
            print("{}. {}".format(idx+1, command_List[idx]), end = ' ')
        print('')
        command = input()
        
        return command
    
    def add_Score(self, score):
        # 스코어 획득
        self.score += score