from pieces import *
from constants import *



class Game:
    
    
    # Checks if the move is blocked by another piece.
    def check_move(self, board, piece, original_position):
        """
        Checks if a move is valid for a given chess piece on the board.

        Args:
            board (list): The chessboard as a 2D list
            piece (object): The chess piece to be moved.
            original_position (tuple): The original position of the piece.

        Returns:
            Boolean: True if move is valid, False otherwise.
        """
        old_row, old_col = original_position
        new_row, new_col = piece.x, piece.y
        num_points = max(abs(new_row - old_row), abs(new_col - old_col))

        # Builds a list of x points in between the original piece position
        # and the new piece position.
        if new_row - old_row == 0:
            x_points = [new_row for _ in range(1, num_points)]
        elif new_row - old_row > 0:
            x_points = [x for x in range(old_row + 1, new_row)]
        else:
            x_points = [x for x in range(old_row - 1, new_row, -1)]

        # Builds a list of y points in between the original piece position
        # and the new piece position.
        if new_col - old_col == 0:
            y_points = [new_col for _ in range(1, num_points)]
        elif new_col - old_col > 0:
            y_points = [y for y in range(old_col + 1, new_col)]
        else:
            y_points =[y for y in range(old_col - 1, new_col, -1)]

        # Combines the x and y lists into a list of points.
        piece_path = list(zip(x_points, y_points))

        # Checks if there is a piece in the move path.
        for point in piece_path:
            if board[point[0]][point[1]] != []:
                self.reset_piece(piece, old_row, old_col)
                return False

        # Checks if it is a valid capture.
        if self.check_capture(board, piece, original_position) == True:
            return True

        self.reset_piece(piece, old_row, old_col)
        return False
    
    def check_capture(self, board, piece, original_position):
        """
        Checks that the pieces only capture pieces of opposite color.

        Args:
            board (list): The chessboard as a 2D list
            piece (object): The chess piece to be moved.
            original_position (tuple): The original position of the piece.

        Returns:
            Boolean: True if capture is valid, False otherwise.
        """
        
        old_row, old_col = original_position
        new_row, new_col = piece.x, piece.y

        # Checks if the piece tries to capture its own color.
        if (board[new_row][new_col]
            and board[new_row][new_col].color == piece.color):
                self.reset_piece(piece, old_row, old_col)
                return False
        
        # Calls pawn capture logic if piece is a pawn.
        if isinstance(piece, Pawn):
            return self.check_pawn_capture(board, piece, new_row, new_col, old_row, old_col)

        return True
        
    def check_pawn_capture(self, board, piece, new_row, new_col, old_row, old_col ):
        """
        Checks for pieces in front of moving pawns and checks for piece when pawn
        tries to capture.

        Args:
            board (list): The chessboard in a 2D list.
            piece (object): The chess piece to be moved.
            new_row (int): Board row to move piece to.
            new_col (int): Board column to move piece to,
            old_row (int): Board row where piece was.
            old_col (int): Board column where piece was.

        Returns:
            boolean: True if capture is valid, False otherwise.
        """
        
        # Check if piece is in front of moving pawn, disallowing movement or capture.
        if (board[new_row][new_col] and new_row == old_row):
            self.reset_piece(piece, old_row, old_col)
            return False
        
        # Checks if pawn tries move to capture square but there is
        # no piece to capture, disallow capture or movement.
        elif not board[new_row][new_col] and new_row != old_row:
            self.reset_piece(piece, old_row, old_col)
            return False
        
        return True
        
    def reset_piece(self, piece, old_row, old_col):
        # Resets the piece position to the square before the move.
        piece.x = old_row
        piece.y = old_col




        
        
