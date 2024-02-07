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

def valid_move(piece, board, new_position, original_position, game, w_king, b_king, player):
    
    if piece.move(new_position, original_position) == False:
        return False
    if game.can_move(board, piece, original_position) == False:
        return False
    
    game.in_check(board, w_king, b_king)
    
    if w_king.check == True and player.color == WHITE:
        return False
    elif b_king.check == True and player.color == BLACK:
        return False
    
    return True