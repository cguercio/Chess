import pygame
import math
from constants import *
from pieces import *
from game import *


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            
# This function converts the mouse position to the position of the board.
def mouse_pos_to_board_pos(pos, board):
    
    num_cols = len(board[0]) # Gets the number of cols by getting the length of the first list
    num_rows = len(board) # Gets the number of rows by getting the number of lists
    square_width = WIDTH // num_cols
    square_height = HEIGHT // num_rows

    return (int(math.floor(pos[0] // square_width)), int(math.floor(pos[1] // square_height)))

def valid_move(piece, board, new_position, original_position, game, player):
    
    old_col, old_row = original_position
    new_col, new_row = new_position
    
    
    if piece.valid_move(new_position, original_position) == False:
        print("2")
        return False
    if game.piece_path(board, new_position, original_position) == False:
        print("3")
        return False
    if game.can_capture(board, new_position, original_position) == False:
        print("4")
        return False
    
    if  board[new_col][new_row] != []:
        board[new_col][new_row].is_captured = True

        
    board[old_col][old_row] = []
    board[new_col][new_row] = piece
    
    for col, rank in enumerate(board):
        for row, item in enumerate(rank):
            if isinstance(item, King) and item.color == WHITE:
                white_king = (col, row)
                w_king = item
            elif isinstance(item, King) and item.color == BLACK:
                black_king = (col, row)
                b_king = item
    
    w_king.is_captured = False
    b_king.is_captured = False
    
    game.in_check(board, white_king, black_king, w_king, b_king)

    if w_king.is_captured == True and player.color == WHITE:
        print("5")
        return False
    elif b_king.is_captured == True and player.color == BLACK:
        print("6")
        return False
    
    piece.move(new_position)
    
    temp_list = []
    for thing in Piece.instances:
        state = (thing.x, thing.y, thing.color, thing.is_captured)
        temp_list.append(state)
        
    Piece.game_state.append(temp_list)
    print(Piece.game_state)
    return True