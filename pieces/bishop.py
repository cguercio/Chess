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
        
        # Checks that the bishop only moves on a diagonal.
        if (abs(new_position[0] - original_position[0]) != abs(new_position[1] - original_position[1])):
            return False
        else:
            self.x = new_position[0]
            self.y = new_position[1]
            return True