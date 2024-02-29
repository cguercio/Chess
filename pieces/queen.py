from pieces import Piece
from constants import *
import math
import os


class Queen(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.col = col
        self.row = row
        self.color = color

        # If color attribute is black, set img attribute to white piece png, white otherwise.
        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_queen_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_queen_png_shadow_100px.png')

    def is_valid_move(self, new_position, original_position):
        """
        Checks that the queen can only move along a diagonal
        or along a row or column.

        Args:
            new_position (tuple): Position to which the piece is to be moved.
            original_position (tuple): Original position of piece.

        Returns:
            boolean: Returns True if move is valid, returns False otherwise.
        """
        
        # Unpacking location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position

        # Defining helper variables.
        not_on_row_or_col = new_col - old_col != 0 and new_row - old_row != 0
        not_on_diagonal = abs(new_col - old_col) != abs(new_row - old_row)
        
        # Checks that the queen only moves along a row or col or along a diagonal.
        if not_on_row_or_col and not_on_diagonal:
            return False

        return True