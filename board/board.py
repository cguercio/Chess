from constants import *
from utils import *
from pieces import *

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

    def update_board(self, piece, new_position, original_position):
        """
        Places the piece at it's new square and clears the old square.

        Args:
            piece (object): Piece being moved.
            new_position (tuple): The new position of the piece
            original_position (_type_): The original position of the piece.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        captured_piece = self.board[new_col][new_row]
        self.board[old_col][old_row] = []
        self.board[new_col][new_row] = piece
        
        return captured_piece
        
    def reset_board(self, piece, new_position, original_position, old_piece=[]):
        # sourcery skip: default-mutable-arg
        """
        Places the piece at it's new square and clears the old square.

        Args:
            piece (object): Piece being moved.
            new_position (tuple): The new position of the piece
            original_position (_type_): The original position of the piece.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        self.board[old_col][old_row] = piece
        self.board[new_col][new_row] = old_piece if old_piece != [] else []
        
    def reset_castling(self, piece, new_position, original_position, i):
        """
        Resets the king castling parameters and resets the board.

        Args:
            piece (object): Piece being moved.
            new_position (tuple): The new position of the piece.
            original_position (tuple): The original position of the piece.
            i (int): Index used during castling.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        piece.in_check = False
        piece.castling = False
        self.board[old_col][old_row] = piece
        self.board[new_col][new_row] = []
        self.board[old_col + i][old_row] = []
    