from pieces import Piece
from constants import *
import os

class King(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.col = col
        self.row = row
        self.color = color
        self.in_check = False
        self.castling = False
        self.has_moved = False

        # If color attribute is black, set img attribute to white piece png, white otherwise.
        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_king_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_king_png_shadow_100px.png')
        
        # Set king positions when the king castles.
        if self.color == BLACK:
            self.castle_left = (2, 0)
            self.castle_right = (6, 0)
        elif self.color == WHITE:
            self.castle_left = (2, 7)
            self.castle_right = (6, 7)

    def is_valid_move(self, new_position, original_position):
        """
        Checks that the king move is only one square in each direction.

        Args:
            new_position (tuple): Position to which the piece is to be moved.
            original_position (tuple): Original position of piece.


        Returns:
            boolean: True if move is valid, False otherwise.
        """
        
        # Unpacking location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position

        # Defining the extents of the board.
        upper_board_extents = 7
        lower_board_extents = 0
        
        # Checks for the piece moving to a square that is not on the board.
        if (new_col > upper_board_extents
            or new_col < lower_board_extents
            or new_row > upper_board_extents
            or new_row < lower_board_extents):
            return False
        
        # Defining helper variables.
        rook_columns = [0, COLUMNS - 1]
        is_in_same_row = abs(new_row - old_row) == 0
        has_not_moved = self.has_moved == False
        has_moved_two_columns = abs(new_col - old_col) == 2
        has_moved_more_than_one_col = abs(new_col - old_col) > 1
        has_moved_more_than_one_row = abs(new_row - old_row) > 1

        # Checks if the king try's to move to the rook for castling.
        if new_col in rook_columns and is_in_same_row and has_not_moved:
            self.castling = True
            return True
            
        # Checks if the king moves two squares for castling.
        if has_moved_two_columns and is_in_same_row and has_not_moved:
            self.castling = True
            return True
        
        # Checks that the king only moves one square.
        if has_moved_more_than_one_col or has_moved_more_than_one_row:
            return False
        
        return True
    
    def move(self, location):
        """
        Sets piece col and row to location passed in.

        Args:
            location (tuple): Location to move to: (col, row)
        """
        self.col, self.row = location
        self.has_moved = True
        