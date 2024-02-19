from pieces import Piece
from constants import *
import math
import os

class Pawn(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color
        self.starting_pos = (x, y)
        self.promotion = False
                
        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_pawn_png_shadow_100px.png')
        elif self.color == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_pawn_png_shadow_100px.png')

    def valid_move(self, new_position, original_position):
        """
        Allows pawns to move only square forward unless it is on
        it's starting square in which case it can move two.
        Allows one square in diagonal movement for captures.   

        Args:
            new_position (tuple): Position to which piece is to be moved.
            original_position (tuple): Original position of piece.

        Returns:
            boolean: Return True if move is valid, False otherwise.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        col_diff = abs(new_col - old_col)
        row_diff = abs(new_row - old_row)
        
        # Check if the pawn is moving only in y.
        if col_diff == 0:
            # Check if pawn is at starting pos and moves more than 2.
            if original_position == self.starting_pos and row_diff > 2:
                return False
            # Check if pawn is not at starting pos and moves more than 1.
            if original_position != self.starting_pos and row_diff > 1:
                return False
            # check if the pawn is moving backwards.
            if self.color == WHITE and new_row - old_row > 0:
                return False
            if self.color == BLACK and new_row - old_row < 0:
                return False
        else:
            # Check if the pawn is moving more than 1 diagonally.
            if col_diff > 1 or row_diff > 1 or col_diff == 1 and row_diff != 1:
                return False
            # check if the pawn trying to capture backwards.
            if self.color == WHITE and new_row - old_row > 0:
                return False
            if self.color == BLACK and new_row - old_row < 0:
                return False
    
    def move(self, new_position):
        self.x, self.y = new_position
