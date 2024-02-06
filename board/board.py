from constants import *
from utils import *

class Board:

    def __init__(self, x_squares, y_squares):
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.board = [[[] for _ in range(x_squares)] for _ in range(y_squares)]

    # Method builds a list of lists of points for squares to be drawn
    def squares(self):
        """
        Returns a list of lists representing the coordinates of each square on the chessboard.

        Args:
            self: The Chessboard instance.

        Returns:
            A list of lists, where each inner list contains the (x, y) coordinates of a square.

        """
        square_width = WIDTH // self.x_squares
        square_height = HEIGHT // self.y_squares

        return [
            [(x, y) for x in range(0, WIDTH, square_width)]
            for y in range(0, HEIGHT, square_height)]

    
    def place_piece(self, piece):
        row, col = piece.x, piece.y
        """
        Places the piece on the board
        
        Args:
            piece: The piece to be placed.
            
        Returns:
            None
        
        """
        # Places the piece on the board.
        self.board[row][col] = piece

    def update_piece(self, piece, original_position):
        """
        Updates the position of a piece on the board.

        Args:
            piece: The piece to be updated.
            original_position: The original position of the piece.

        Returns:
            None
        """
        old_row, old_col = original_position
        new_row, new_col = piece.x, piece.y
        
        # Removes a piece from its original position.
        self.board[old_row][old_col] = []
        
        # Places the piece at its new position.
        self.board[new_row][new_col] = piece
