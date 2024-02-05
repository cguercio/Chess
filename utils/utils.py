import pygame
import math
from constants import *


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            
# This function converts the mouse position to the position of the board.
def mouse_pos_to_board_pos(pos, board):
    num_cols = len(board[0]) # Gets the number of cols by geting the length of the first list
    num_rows = len(board) # Gets the number of rows by getting the number of lists

    new_posisition = (int(math.floor(pos[0] // (WIDTH // num_cols))),
                       int(math.floor(pos[1] // (HEIGHT // num_rows))))

    return new_posisition