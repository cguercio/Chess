import os
from constants import *

class Piece:
    instances = []
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        Piece.instances.append(self)
        
    def get_promotion_pieces(self, piece):
        """
        Creates a list of null pieces so their images can be displayed.

        Args:
            piece (obkect): Piece being promoted.

        Returns:
            list: List of piece objects.
        """

        
        from .rook import Rook
        from .knight import Knight
        from .bishop import Bishop
        from .queen import Queen

        if piece.color == BLACK:
            promotion_pieces = [Piece.Queen(None, None, piece.color),
                                Rook(None, None, piece.color),
                                Bishop(None, None, piece.color),
                                Knight(None, None, piece.color)
            ]
            
        elif piece.color  == WHITE:
            promotion_pieces = [Queen(None, None, piece.color),
                                Rook(None, None, piece.color),
                                Bishop(None, None, piece.color),
                                Knight(None, None, piece.color)
            ]
            
        return promotion_pieces