from tkinter import image_names
import math
import cv2
import os
from main import LittleBattle
from utilities import print_board

class GUI_file:
    p1_homebase = cv2.imread('./resource/tile_P1HomeBase.png')
    p1_homebase = cv2.resize(p1_homebase,(128,128))
    p2_homebase = cv2.imread('./resource/tile_P2HomeBase.png')
    p2_homebase = cv2.resize(p2_homebase,(128,128))

    tile_ground = cv2.imread('./resource/tile_ground.png')
    tile_ground = cv2.resize(tile_ground,(128,128))
    tile_poison = cv2.imread('./resource/tile_poison.png')
    tile_poison = cv2.resize(tile_poison,(128,128))
    tile_water = cv2.imread('./resource/tile_water.png')
    tile_water = cv2.resize(tile_water,(128,128))

    ground_wood = cv2.imread('./resource/ground_wood.png')
    ground_wood = cv2.resize(ground_wood,(128,128))
    ground_food = cv2.imread('./resource/ground_food.png')
    ground_food = cv2.resize(ground_food,(128,128))
    ground_gold = cv2.imread('./resource/ground_gold.png')
    ground_gold = cv2.resize(ground_gold,(128,128))
    # ----------------------------------------------------
    poison_wood = cv2.imread('./resource/poison_wood.png')
    poison_wood = cv2.resize(poison_wood,(128,128))
    poison_food = cv2.imread('./resource/poison_food.png')
    poison_food = cv2.resize(poison_food,(128,128))
    poison_gold = cv2.imread('./resource/poison_gold.png')
    poison_gold = cv2.resize(poison_gold,(128,128))
    # ----------------------------------------------------
    water_wood = cv2.imread('./resource/water_wood.png')
    water_wood = cv2.resize(water_wood,(128,128))
    water_food = cv2.imread('./resource/water_food.png')
    water_food = cv2.resize(water_food,(128,128))
    water_gold = cv2.imread('./resource/water_gold.png')
    water_gold = cv2.resize(water_gold,(128,128))

    # ----------------------------------------------------
    ground_A1 = cv2.imread('./resource/ground_A_P1.png')
    ground_A1 = cv2.resize(ground_A1,(128,128))
    ground_S1 = cv2.imread('./resource/ground_S_P1.png')
    ground_S1 = cv2.resize(ground_S1,(128,128))
    ground_K1 = cv2.imread('./resource/ground_K_P1.png')
    ground_K1 = cv2.resize(ground_K1,(128,128))
    ground_C1 = cv2.imread('./resource/ground_C_P1.png')
    ground_C1 = cv2.resize(ground_C1,(128,128))
    
    water_C1 = cv2.imread('./resource/water_C_P1.png')
    water_C1 = cv2.resize(water_C1,(128,128))
    # ----------------------------------------------------
    ground_A2 = cv2.imread('./resource/ground_A_P2.png')
    ground_A2 = cv2.resize(ground_A2,(128,128))
    ground_S2 = cv2.imread('./resource/ground_S_P2.png')
    ground_S2 = cv2.resize(ground_S2,(128,128))
    ground_K2 = cv2.imread('./resource/ground_K_P2.png')
    ground_K2 = cv2.resize(ground_K2,(128,128))
    ground_C2 = cv2.imread('./resource/ground_C_P2.png')
    ground_C2 = cv2.resize(ground_C2,(128,128))
    
    water_C2 = cv2.imread('./resource/water_C_P2.png')
    water_C2 = cv2.resize(water_C2,(128,128))
        # ----------------------------------------------------

def _locate_image(tile_type,resource_type,soldier_type):

        if tile_type == 'P1':
            tile_image = GUI_file.p1_homebase
        elif tile_type == 'P2':
            tile_image = GUI_file.p2_homebase

        elif soldier_type !='N/A':
            if '1' in soldier_type:
                if 'Archer' in soldier_type:
                    tile_image = GUI_file.ground_A1
                elif 'Knight' in soldier_type:
                    tile_image = GUI_file.ground_K1
                elif 'Spearman' in soldier_type:
                    tile_image = GUI_file.ground_S1
                elif 'Scout' in soldier_type:
                    if tile_type =='2':
                        tile_image = GUI_file.water_C1
                    else:
                        tile_image = GUI_file.ground_C1

            elif '2' in soldier_type:
                if 'Archer' in soldier_type:
                    tile_image = GUI_file.ground_A2
                elif 'Knight' in soldier_type:
                    tile_image = GUI_file.ground_K2
                elif 'Spearman' in soldier_type:
                    tile_image = GUI_file.ground_S2
                elif 'Scout' in soldier_type:
                    if tile_type =='2':
                        tile_image = GUI_file.water_C2
                    else:
                        tile_image = GUI_file.ground_C2
                
        
        else:
            if tile_type == '0':
                if resource_type == '0':
                    tile_image = GUI_file.tile_ground
                elif resource_type == 'F':
                    tile_image = GUI_file.ground_food
                elif resource_type == 'G':
                    tile_image = GUI_file.ground_gold
                elif resource_type == 'W':
                    tile_image = GUI_file.ground_wood
            elif tile_type == '1':
                if resource_type == '0':
                    tile_image = GUI_file.tile_poison
                elif resource_type == 'F':
                    tile_image = GUI_file.poison_food
                elif resource_type == 'G':
                    tile_image = GUI_file.poison_gold
                elif resource_type == 'W':
                    tile_image = GUI_file.poison_wood
            elif tile_type == '2':
                if resource_type == '0':
                    tile_image = GUI_file.tile_water
                elif resource_type == 'F':
                    tile_image = GUI_file.water_food
                elif resource_type == 'G':
                    tile_image = GUI_file.water_gold
                elif resource_type == 'W':
                    tile_image = GUI_file.water_wood
            else:
                print("error")

        return tile_image

def generate_game_board(board):
    '''
    args
        board (dict): ???
        e.g. board[0][0]={
        'reosurce':
        'tile':
        'locate':
        }

    return 
        image(np.ndarray)
    '''

    height = len(list(board.keys()))
    width = len(list(board[0].keys()))
    image_list = []
    print(height,width)

    for y_loc in range(height):
        for x_loc in range (width):
            if board[y_loc][x_loc]['locate']=='P1' or board[y_loc][x_loc]['locate']=='P2':
                image_type = board[y_loc][x_loc]['locate']
            else:
                image_type = board[y_loc][x_loc]['tile']

            soldier_type = board[y_loc][x_loc]['locate']
            resource_type = board[y_loc][x_loc]['resource']

            if x_loc == 0:
                image_list.append(_locate_image(image_type,resource_type,soldier_type))
            else:
                image_list[y_loc] = cv2.hconcat([image_list[y_loc],_locate_image(image_type,resource_type,soldier_type)])

        if y_loc==0:
            image = image_list[y_loc]
        else:
            image = cv2.vconcat([image,image_list[y_loc]])
        

    cv2.imshow('window',image)
    cv2.waitKey(0)

if __name__ == '__main__':
    app = LittleBattle('./game_log1.txt')
    
    board = app.board
    board[0][0]['locate']='Archer1'
    board[1][0]['locate']='Scout2'
    print_board(board)
    generate_game_board(board)