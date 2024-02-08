from pieces import Piece
from constants import *
import math
import os

class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color

        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_knight_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_knight_png_shadow_100px.png')

    def valid_move(self, new_position, original_position):
        """
        Checks that the knight moves either two squares in one
        direction and one in the other.

        Args:
            new_position (tuple): Position to which piece is to be moved.
            original_position (tuple): Original position of piece.

        Returns:
            boolean: True if move is valid, False otherwise.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        col_diff = abs(new_col - old_col)
        row_diff = abs(new_row - old_row)
        
        # Checks that the knight moves either two squares in one
        # direction and one in the other.
        if (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2):
            return True

        return False
    
    def move(self, new_position):
        self.x, self.y = new_position
        
    def check_capture(self):
        """
        Checks if the piece has been captured and 
        changes removes the piece from the piece list.
        """
        if self.is_captured:
            Piece.instances.remove(self)
            
        
