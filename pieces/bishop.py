from pieces import Piece
from constants import *
import math
import os

class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color

        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_bishop_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_bishop_png_shadow_100px.png')

    def move(self, new_position, original_position):
        """
        Checks that the bishop moves only on diagonals.

        Args:
            new_position (tuple): Position to which the piece is to be moved.
            original_position (tuple): Original position of piece.

        Returns:
            boolean: True if move is valid, False otherwise.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        # Checks that the bishop only moves on a diagonal.
        if (abs(new_col - old_col) != abs(new_row - old_row)):
            return False

        self.x = new_col
        self.y = new_row
        return True
    
    def check_capture(self):
        """
        Checks if the piece has been captured and 
        changes removes the piece from the piece list.
        """
        if self.is_captured:
            Piece.instances.remove(self)