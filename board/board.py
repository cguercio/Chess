from constants import *
from utils import *

class Board:
    board_list = []

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
        """
        Places the piece on the board
        
        Args:
            piece: The piece to be placed.
            
        Returns:
            None
        
        """
        col, row = piece.x, piece.y
        # Places the piece on the board.
        self.board[col][row] = piece

    def update_board(self, pieces):
        """
        Updates the position of a piece on the board.

        Args:
            piece: The piece to be updated.
            original_position: The original position of the piece.

        Returns:
            None
        """

        self.board = [[[] for _ in range(self.x_squares)] for _ in range(self.y_squares)]
        
        for item in pieces:
            self.board[item.x][item.y] = item
        self.board_list.append(self.board)

        # old_col, old_row = original_position
        # new_col, new_row = piece.x, piece.y
        
        # # Removes a piece from its original position.
        # self.board[old_col][old_row] = []
        
        # # Places the piece at its new position.
        # self.board[new_col][new_row] = piece
