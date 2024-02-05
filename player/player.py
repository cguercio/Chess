from pieces import *
from constants import *
import pygame

class Player:
    def __init__(self):
        pass

    def move(self, pos, board):
        num_cols = len(board[0]) # Gets the number of cols by geting the length of the first list
        num_rows = len(board) # Gets the number of rows by getting the number of lists
        original_position = (0,0)
        
        for row in board:
            for piece in row:
                if isinstance(piece, Piece):
                    if (pos[0] > piece.x * WIDTH // num_cols 
                        and pos[0] < piece.x * WIDTH // num_cols + WIDTH // num_cols
                        and pos[1] > piece.y * HEIGHT // num_rows 
                        and pos[1] < piece.y * HEIGHT // num_rows + HEIGHT // num_rows):
                        original_position = (piece.x, piece.y)
                        
                        return True, piece, original_position

        return False, piece, original_position