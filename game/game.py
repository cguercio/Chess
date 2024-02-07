from pieces import *
from constants import *
from player import *




class Game:
    
    # Checks if the move is blocked by another piece.
    def can_move(self, board, piece, original_position):
        """
        Checks if a move is valid for a given chess piece on the board.

        Args:
            board (list): The chessboard as a 2D list
            piece (object): The chess piece to be moved.
            original_position (tuple): The original position of the piece.

        Returns:
            Boolean: True if move is valid, False otherwise.
        """
        old_col, old_row = original_position
        new_col, new_row = piece.x, piece.y
        num_points = max(abs(new_col - old_col), abs(new_row - old_row))

        # Builds a list of x points in between the original piece position
        # and the new piece position.
        if new_col - old_col == 0:
            x_points = [new_col for _ in range(1, num_points)]
        elif new_col - old_col > 0:
            x_points = [x for x in range(old_col + 1, new_col)]
        else:
            x_points = [x for x in range(old_col - 1, new_col, -1)]

        # Builds a list of y points in between the original piece position
        # and the new piece position.
        if new_row - old_row == 0:
            y_points = [new_row for _ in range(1, num_points)]
        elif new_row - old_row > 0:
            y_points = [y for y in range(old_row + 1, new_row)]
        else:
            y_points =[y for y in range(old_row - 1, new_row, -1)]

        # Combines the x and y lists into a list of points.
        piece_path = list(zip(x_points, y_points))
        
        for pieces in Piece.instances:
            if (pieces.x, pieces.y) in piece_path:
                self.reset_piece(piece, old_col, old_row)
                return False
                

        # Checks if a piece is trying to capture and if it is a valid capture.
        if (board[new_col][new_row] and
        self.can_capture(board, piece, new_col, new_row) == False):
            self.reset_piece(piece, old_col, old_row)
            return False
        
        # Calls pawn capture logic if piece is a pawn.
        if isinstance(piece, Pawn):
            return self.pawn_can_capture(board, piece, new_col, new_row, old_col, old_row)
        
        return True
    
    def can_capture(self, board, piece, new_col, new_row):
        """
        Checks that the pieces only capture pieces of opposite color.

        Args:
            board (list): The chessboard as a 2D list
            piece (object): The chess piece to be moved.
            original_position (tuple): The original position of the piece.

        Returns:
            Boolean: True if capture is valid, False otherwise.
        """
        
        # Checks if the piece tries to capture its own color.
        if board[new_col][new_row].color == piece.color:
                return False
        
        self.update_capture(board, new_col, new_row)
        return True
        
    def pawn_can_capture(self, board, piece, new_col, new_row, old_col, old_row):
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
        if (board[new_col][new_row] and new_col == old_col):
            self.reset_piece(piece, old_col, old_row)
            return False
        
        # Checks if pawn tries move to capture square but there is
        # no piece to capture, disallow capture or movement.
        elif not board[new_col][new_row] and new_col != old_col:
            self.reset_piece(piece, old_col, old_row)
            return False
        
        print(board[new_col][new_row])
        print(board)
        self.update_capture(board, new_col, new_row)        
        return True
    
    def in_check(self, board, w_king, b_king):
        """
        Checks both kings for check and sets check
        attribute to True if necessary.

        Args:
            board (list): Chess board as a 2D list.
            w_king (object): White king.
            b_king (object): Black king.
        """
        
        # Getting king's positions.
        white_king = (w_king.x, w_king.y)
        black_king = (b_king.x, b_king.y)

        # Looping thought piece objects.
        for piece in Piece.instances:
            old_col, old_row = piece.x, piece.y
            # Trying to move all black pieces to the white king.
            if (piece.color == BLACK and piece.move((white_king), (piece.x, piece.y)) == True
                and self.can_move(board, piece, (old_col, old_row)) == True):
                self.reset_piece(piece, old_col, old_row)
                w_king.check = True
                print("White in check.")

            elif (piece.color == WHITE and piece.move((black_king), (piece.x, piece.y)) == True
                and self.can_move(board, piece, (old_col, old_row)) == True):
                self.reset_piece(piece, old_col, old_row)
                b_king.check = True
                print("Black in check.")
                return

            # Trying to move all white pieces to the black king.
            
        w_king.check = False
        b_king.check = False
        
    def update_capture(self, board, new_col, new_row):
        """
        Tries to sets the object's is_captured attribute to true.

        Args:
            board (list): Chess board represented as a 2D list.
            new_col (int): New piece column
            new_row (int): New piece row.
        """
        try:
            board[new_col][new_row].is_captured = True
            board[new_col][new_row].check_capture()
        except Exception:
            pass

    def reset_piece(self, piece, old_col, old_row):
        """
        Resets the piece back to its original square.

        Args:
            piece (object): Piece to be reset.
            old_col (int): Old piece column.
            old_row (int): Old piece row.
        """
        # Resets the piece position to the square before the move.
        piece.x = old_col
        piece.y = old_row




        
        
