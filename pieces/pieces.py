from constants import *

class Piece:
    instances = []
    
    def __init__(self, col, row, color):
        self.col = col
        self.row = row
        self.color = color
        Piece.instances.append(self)
        
    def get_promotion_pieces(self, piece):
        """
        Creates a list of null pieces so their images can be displayed.

        Args:
            piece (object): Piece being promoted.

        Returns:
            list: List of piece objects.
        """

        # Importing piece classes.
        from .rook import Rook
        from .knight import Knight
        from .bishop import Bishop
        from .queen import Queen

        # Defining black pieces to display promotion images.
        if piece.color == BLACK:
            promotion_pieces = [Piece.Queen(None, None, piece.color),
                                Rook(None, None, piece.color),
                                Bishop(None, None, piece.color),
                                Knight(None, None, piece.color)
            ]

        # Defining white pieces to display promotion images. 
        elif piece.color  == WHITE:
            promotion_pieces = [Queen(None, None, piece.color),
                                Rook(None, None, piece.color),
                                Bishop(None, None, piece.color),
                                Knight(None, None, piece.color)
            ]
        
        return promotion_pieces
    
    def move(self, location):
        """
        Sets the piece locations to the location passed in.

        Args:
            location (tuple): Location to be moved: (col, row)
        """
        self.col, self.row = location