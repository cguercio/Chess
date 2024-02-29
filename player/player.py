from pieces import *
from constants import *


class Player:
    pass
    # def move(self, board_position, board):
    #     """
    #     Checks if the player clicked on a piece.

    #     Args:
    #         click_position (tuple): Position on the board where the player clicked.
    #         board (list): 2D list representing the board.

    #     Returns:
    #         bool, object, tuple: True if player clicked on piece, False if not. Piece clicked on and piece position.
    #     """

    #     # Unpacking location tuples.
    #     col, row = board_position
        
    #     # Defining variables so they are not None.
    #     original_position = (0,0)
    #     piece = board[col][row]
        
    #     # True if there board position contains a piece.
    #     piece_on_square = board[col][row] != []
        
    #     # Checks if a piece is on square.
    #     if piece_on_square:
            
    #         # Retrieves the clicked piece and its position.
    #         piece = board[col][row]
    #         original_position = (piece.col, piece.row)
            
    #         return True, piece, original_position

    #     return False, piece, original_position