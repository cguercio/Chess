from pieces.pieces import Piece
from constants import *
import os

class Bishop(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.col = col
        self.row = row
        self.color = color

        # If color attribute is black, set img attribute to white piece png. White otherwise.
        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_bishop_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_bishop_png_shadow_100px.png')

    def is_valid_move(self, new_position, original_position):
        """
        Checks that the bishop moves only on diagonals.

        Args:
            new_position (tuple): Position to which the piece is to be moved.
            original_position (tuple): Original position of piece.

        Returns:
            boolean: True if move is valid, False otherwise.
        """
        
        # Defining the extents of the board.
        upper_board_extents = 7
        lower_board_extents = 0
        
        # Unpacking location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position

        # The row and column difference are not equal if piece doesn't move on a diagonal.
        not_on_diagonal = (abs(new_col - old_col) != abs(new_row - old_row))
        
        # Checks that the bishop only moves on a diagonal.
        if not_on_diagonal:
            return False

        return True
    
