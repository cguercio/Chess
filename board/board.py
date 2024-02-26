from constants import *
from utils import *
from pieces import *
import math

class Board:
    board_list = []

    def __init__(self, cols, rows, width, height):
        self.cols = cols
        self.rows = rows
        self.width = width
        self.height = height
        self.board = [[[] for _ in range(cols)] for _ in range(rows)]
        self.square_width = self.width // self.cols
        self.square_height = self.height // self.rows
        
    def squares(self):
        """
        Returns a list of lists representing the coordinates of each square on the chessboard.

        Args:
            self: The Chessboard instance.

        Returns:
            A list of lists, where each inner list contains the (x, y) coordinates of a square.

        """
        
        # Building lists of columns and rows depending on the screen and square width and height.
        col_start_points = range(0, self.width, self.square_width)
        row_start_points = range(0, self.height, self.square_height)
        
        # Returns a list of lists representing the board.
        return [
            [(col, row) for col in col_start_points]
            for row in row_start_points]

    
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
            
    def get_board_position(self, mouse_position):
        """
        Converts the mouse position to the board position.

        Args:
            pos (tuple): Mouse position.
            board (list): Chessboard as a 2D list.

        Returns:
            tuple: Returns the new board position.
        """
        
        board_col = int(math.floor(mouse_position[0] // self.square_width))
        board_row = int(math.floor(mouse_position[1] // self.square_height))

        return board_col, board_row
    
    def get_square_contents(self, board_position):
        """
        Checks if the player clicked on a piece.

        Args:
            board_position (tuple): Position on the board where the player clicked: (col, row)

        Returns:
            bool, object, tuple: True if player clicked on piece, False if not. Piece clicked on and piece position.
        """

        # Unpacking location tuples.
        col, row = board_position

        contents = self.board[col][row]

        return contents
        
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
        Places the piece at its original position, resets the new position square.

        Args:
            piece (object): Piece being moved.
            new_position (tuple): New position of piece: (col, row)
            original_position (tuple): Original position of piece: (col, row)
            old_piece (object, optional): Piece being captured or empty list if no piece. Defaults to [].
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
    