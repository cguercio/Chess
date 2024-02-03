from pieces import Piece
import math

class Rook(Piece):
    
    def move(self, pos):
        self.x = int(math.floor(pos[0]/100))
        self.y = int(math.floor(pos[1]/100))
        
