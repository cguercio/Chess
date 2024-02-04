from pieces import Piece
from constants import *
import math

class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color

        if self.color == BLACK:
            self.img = 'D:\Coding\Cloned Repositories\Chess\graphics\\b_queen_png_shadow_100px.png'
        elif self.color  == WHITE:
            self.img = 'D:\Coding\Cloned Repositories\Chess\graphics\\w_queen_png_shadow_100px.png'

    def move(self, pos):
        self.x = int(math.floor(pos[0]/100))
        self.y = int(math.floor(pos[1]/100))