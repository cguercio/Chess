from pieces import *
from constants import *
import pygame

class Player:
    def __init__(self, turn, color):
        self.turn = turn
        self.color = color

    def move(self, pos, board):
        num_cols = len(board[0]) # Gets the number of cols by getting the length of the first list
        num_rows = len(board) # Gets the number of rows by getting the number of lists
        square_width = WIDTH // num_cols
        square_height = HEIGHT // num_rows
        
        original_position = (0,0) # This is a place holder so this variable does not return none until move loop is in place.
        
        for row in board:
            for piece in row:
                if (isinstance(piece, Piece) and (pos[0] > piece.x * square_width 
                                                  and pos[0] < piece.x * square_width + square_width 
                                                  and pos[1] > piece.y * square_height 
                                                  and pos[1] < piece.y * square_height + square_height)):
                    
                    original_position = (piece.x, piece.y)
                    return True, piece, original_position

        return False, piece, original_position