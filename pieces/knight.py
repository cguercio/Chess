from pieces import Piece
from constants import *
import math
import os

class Knight(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.col = col
        self.row = row
        self.color = color

        # If color attribute is black, set img attribute to white piece png, white otherwise.
        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_knight_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_knight_png_shadow_100px.png')

    def is_valid_move(self, new_position, original_position):
        """
        Checks that the knight moves either two squares in one
        direction and one in the other.

        Args:
            new_position (tuple): Position to which piece is to be moved.
            original_position (tuple): Original position of piece.

        Returns:
            boolean: True if move is valid, False otherwise.
        """
        
        # Unpacking location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position

        # Defining helper variables.
        col_diff = abs(new_col - old_col)
        row_diff = abs(new_row - old_row)
        has_moved_two_cols = col_diff == 2
        has_moved_one_row = row_diff == 1
        has_moved_two_rows = row_diff == 2
        has_moved_one_col = col_diff == 1
        
        # Checks that the knight moves two squares in one
        # direction and one in the other.
        if ((has_moved_two_cols and has_moved_one_row)
            or (has_moved_one_col and has_moved_two_rows)):
            return True

        return False