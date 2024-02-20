from pieces import Piece
from constants import *
import math
import os

class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color
        self.in_check = False
        self.castling = False
        self.has_moved = False

        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_king_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_king_png_shadow_100px.png')

    def valid_move(self, new_position, original_position):
        """
        Checks that the king move is only one square in each direction.

        Args:
            new_position (tuple): Position to which the piece is to be moved.
            original_position (_type_): Original position of piece.


        Returns:
            boolean: True if move is valid, False otherwise.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        if new_col > 7 or new_col < 0 or new_row > 7 or new_row < 0:
            return False
        
        if new_col in [0, COLUMNS - 1] and abs(new_row - old_row) == 0 and self.has_moved == False:
            self.castling = True
            return True
            
        # Checks if the king is trying to castle.
        if abs(new_col - old_col) == 2 and abs(new_row - old_row) == 0 and self.has_moved == False:
            self.castling = True
            return True
        
        # Checks that the king only moves one square.
        if (abs(new_col - old_col) > 1 or abs(new_row - old_row) > 1):
            return False
        
        return True
    
    def move(self, new_position):
        self.x, self.y = new_position
        self.has_moved = True
        