from pieces import Piece
from constants import *
import math
import os

class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color

        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics',
                                                'b_rook_png_shadow_100px.png')
        elif self.color  == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics',
                                                'w_rook_png_shadow_100px.png')

    def move(self, pos, original_position):

        # Converts the mouse position to the new board
        # position by rounding it down to the nearest 100.
        new_posisition = (int(math.floor(pos[0]/100)),
                           int(math.floor(pos[1]/100)))
        
        if (new_posisition[0] - original_position[0] != 0 
            and new_posisition[1] - original_position[1] != 0):
            return False
        else:
            self.x = new_posisition[0]
            self.y = new_posisition[1]
            return True
