from constants import *
from utils import *
from pieces import *

class Board:
    board_list = []

    def __init__(self, x_squares, y_squares):
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.board = [[[] for _ in range(x_squares)] for _ in range(y_squares)]

    def squares(self):
        """
        Returns a list of lists representing the coordinates of each square on the chessboard.

        Args:
            self: The Chessboard instance.

        Returns:
            A list of lists, where each inner list contains the (x, y) coordinates of a square.

        """
        # Calculating square height and width.
        square_width = WIDTH // self.x_squares
        square_height = HEIGHT // self.y_squares

        # Returns a list of lists representing the board.
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

        col, row = piece.col, piece.row

        # Set the pieces at their locations on the board.
        if col is not None and row is not None:
            self.board[col][row] = piece
        
    def update_board(self, piece, new_position, original_position):
        """
        Places the piece at it's new square and clears the old square.

        Args:
            piece (object): Piece being moved.
            new_position (tuple): The new position of the piece
            original_position (_type_): The original position of the piece.
        """
        
        # Unpacking the location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position

        # Setting "captured_piece" to the new board position
        captured_piece = self.board[new_col][new_row]

        # Clear the piece old square and set it at its new square.
        self.board[old_col][old_row] = []
        self.board[new_col][new_row] = piece
        
        return captured_piece
        
    def reset_board(self, piece, new_position, original_position, old_piece=[]):
        """
        Places the piece at it's new square and clears the old square.

        Args:
            piece (object): Piece being moved.
            new_position (tuple): The new position of the piece
            original_position (_type_): The original position of the piece.
        """
        
        # Unpacking the location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        # Put the old piece back to its original location put the old piece back.
        self.board[old_col][old_row] = piece
        self.board[new_col][new_row] = old_piece
        
    def reset_castling(self, piece, new_position, original_position, i):
        """
        Resets the king castling parameters and resets the board.

        Args:
            piece (object): Piece being moved.
            new_position (tuple): The new position of the piece.
            original_position (tuple): The original position of the piece.
            i (int): Index used during castling.
        """
        # Unpacking the location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        # Reset the castling attributes.
        piece.in_check = False
        piece.castling = False

        # Reset the board.
        self.board[old_col][old_row] = piece
        self.board[new_col][new_row] = []
        self.board[old_col + i][old_row] = []
    