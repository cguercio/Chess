from pieces import Piece
from constants import *
import os

class Pawn(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.col = col
        self.row = row
        self.color = color
        self.starting_pos = (col, row)
        self.promotion = False
        self.enpassant = False
        
        # If color attribute is black, set img attribute to white piece png, white otherwise.
        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_pawn_png_shadow_100px.png')
        elif self.color == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_pawn_png_shadow_100px.png')

    def is_valid_move(self, new_position, original_position):
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
        
        # Unpacking location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position

        # Defining helper variables.
        col_diff = abs(new_col - old_col)
        row_diff = abs(new_row - old_row)
        pawn_is_white = self.color == WHITE
        pawn_is_black = self.color == BLACK
        row_diff_is_positive = new_row - old_row > 0
        row_dif_is_negative = new_row - old_row < 0
        is_in_same_column = col_diff == 0
        has_moved = original_position != self.starting_pos
        moved_more_than_two_rows = row_diff > 2
        moved_more_than_one_row = row_diff > 1
        moved_more_than_one_diagonal = col_diff > 1 or row_diff > 1
        moved_not_on_diagonal = col_diff == 1 and row_diff != 1

        # check if the pawn is moving backwards.
        if pawn_is_white and row_diff_is_positive:
            return False
        if pawn_is_black and row_dif_is_negative:
            return False

        # Check if the pawn is moving only in y.
        if is_in_same_column:
            # Check if pawn is at starting pos and moves more than 2.
            if not has_moved and moved_more_than_two_rows:
                return False
            # Check if pawn is not at starting pos and moves more than 1.
            if has_moved and moved_more_than_one_row:
                return False
        else:
            # Check if the pawn is moving more than 1 diagonally.
            if moved_more_than_one_diagonal or moved_not_on_diagonal:
                return False
            
        return True