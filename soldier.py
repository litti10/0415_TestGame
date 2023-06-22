class Soldier:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type
        self.movable = False
    
    @staticmethod
    def get_cost_dict():
        dic_soliderCost = {
            'Archer': {
                'gold': 0,
                'wood': 1,
                'food': 1
            },
            'Spearman':{
                'gold': 1,
                'wood': 1,
                'food': 0
            },
            'Knight': {
                'gold': 1,
                'wood': 0,
                'food': 1
            },
            'Scout':{
                'gold': 1,
                'wood': 1,
                'food': 1
            }
        }
        return dic_soliderCost
    
    def fight(self, my_sol, other_sol):
        win_dict = {
            'Scout': 0,
            'Archer': 1,
            'Spearman': 2,
            'Knight': 3
        }
        
        exepction_ArcherWinKnight = False
        if my_sol == 'archer' and other_sol == 'knight':
            exepction = True

        if win_dict[my_sol] > win_dict[other_sol] or exepction_ArcherWinKnight:
            return "win"
        elif win_dict[my_sol] < win_dict[other_sol]:
            return "lose"
        elif win_dict[my_sol] == win_dict[other_sol]:
            return "tie"