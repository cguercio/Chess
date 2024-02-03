from pieces import *
from constants import *
import pygame

class Player:
    def __init__(self):
        pass

    def move(self, pos, board):
        num_cols = len(board[0]) # Gets the number of cols by geting the length of the first list
        num_rows = len(board) # Gets the number of rows by getting the number of lists
        old_peice_x = 0
        old_peice_y = 0

        for row in board:
            for piece in row:
                if isinstance(piece, Piece):
                    if (pos[0] > piece.x * WIDTH // num_cols 
                        and pos[0] < piece.x * WIDTH // num_cols + WIDTH // num_cols
                        and pos[1] > piece.y * HEIGHT // num_rows 
                        and pos[1] < piece.y * HEIGHT // num_rows + HEIGHT // num_rows):
                        old_peice_x = piece.x
                        old_peice_y = piece.y

                        
                        return True, piece, old_peice_x, old_peice_y

        return False, piece, old_peice_x, old_peice_y
                        