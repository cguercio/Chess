from pieces import Piece
from constants import *
import math
import os

class Pawn(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color
        self.starting_pos = (x, y)

        if self.color == BLACK:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'b_pawn_png_shadow_100px.png')
        elif self.color == WHITE:
            self.img = os.path.join(os.path.dirname(__file__),'..','graphics', 'w_pawn_png_shadow_100px.png')

    def move(self, new_position, original_position):

        # Checks if the pawn is on its first move then allows it to move one or two squares.
        # If the pawn is not on its first move, then checks for only one more forward.
        # Allows the pawn to move forward diagonally for one square to allow for captures.
        if self.color == WHITE: # Checks for white pawns
            if (original_position == self.starting_pos
                and new_position[1] - original_position[1] in (-2, -1)):
                if (new_position[1] - original_position[1] == -2
                    and new_position[0] - original_position[0] == 0):
                    self.x = new_position[0]
                    self.y = new_position[1]
                    return True 
                
                elif (new_position[1] - original_position[1] == -1
                    and new_position[0] - original_position[0] in (-1, 0, 1)):
                    self.x = new_position[0]
                    self.y = new_position[1]
                    return True
                
                else:
                    return False
                
            elif (new_position[1] - original_position[1] == -1 
                    and new_position[0] - original_position[0] in (-1, 0, 1)):
                self.x = new_position[0]
                self.y = new_position[1]
                return True

        # Checks for black pawns
        elif (original_position == self.starting_pos 
              and new_position[1] - original_position[1] in (2, 1)):
            if (new_position[1] - original_position[1] == 2 
                and new_position[0] - original_position[0] == 0):
                self.x = new_position[0]
                self.y = new_position[1]
                return True 
            
            elif (new_position[1] - original_position[1] == 1
                  and new_position[0] - original_position[0] in (-1, 0, 1)):
                self.x = new_position[0]
                self.y = new_position[1]
                return True
            
            else:
                return False
            
        elif (new_position[1] - original_position[1] == 1
              and new_position[0] - original_position[0] in (-1, 0, 1)):
            self.x = new_position[0]
            self.y = new_position[1]
            return True 
        
        else:
            return False