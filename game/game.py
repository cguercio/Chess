from pieces import *
from constants import *
from player import *
from graphics import *




class Game:
    
    # Checks if the move is blocked by another piece.
    def piece_path(self, board, new_position, original_position):
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
        new_col, new_row = new_position
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
        
        for point in piece_path:
            if board[point[0]][point[1]] != []:
                return False

        return True
    
    def can_capture(self, board, new_position, original_position):
        """
        Checks that the pieces only capture pieces of opposite color.

        Args:
            board (list): The chessboard as a 2D list
            piece (object): The chess piece to be moved.
            original_position (tuple): The original position of the piece.

        Returns:
            Boolean: True if capture is valid, False otherwise.
        """
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        # Checks if a piece is trying to capture and if it is a valid capture.
        if board[new_col][new_row] != [] and board[new_col][new_row].color == board[old_col][old_row].color:
            return False
        
        # Calls pawn capture logic if piece is a pawn.
        if isinstance(board[old_col][old_row], Pawn):
            return self.pawn_can_capture(board, new_position, original_position)
        
        return True
        
    def pawn_can_capture(self, board, new_position, original_position):
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
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        # Check if piece is in front of moving pawn, disallowing movement or capture.
        if (board[new_col][new_row] and new_col == old_col):
            return False
        
        # Checks if pawn tries move to capture square but there is
        # no piece to capture, disallow capture or movement.
        elif not board[new_col][new_row] and new_col != old_col:
            return False
        
        # self.update_capture(board, new_col, new_row)        
        return True
    
    def in_check(self, board, white_king, black_king, w_king, b_king):
        """
        Checks both kings for check and sets check
        attribute to True if necessary.

        Args:
            board (list): Chess board as a 2D list.
            w_king (object): White king.
            b_king (object): Black king.
        """

        w_king.in_check = False
        b_king.in_check = False
        
        # Looping thought piece objects.
        for col, rank in enumerate(board):
            for row, piece in enumerate(rank):
                if piece != []:
                    original_position = (col, row)
                    # Trying to move all black pieces to the white king.
                    if (piece.color == BLACK and piece.valid_move(white_king, original_position) == True
                        and self.piece_path(board, white_king, original_position) == True
                        and self.can_capture(board, white_king, original_position) == True):
                        print("white in check")
                        w_king.in_check = True

                    # Trying to move all white pieces to the black king.
                    elif (piece.color == WHITE and piece.valid_move(black_king, original_position) == True
                        and self.piece_path(board, black_king, original_position) == True
                        and self.can_capture(board, black_king, original_position) == True):
                        b_king.in_check = True
                        print("black in check")

    def castling(self, screen, game, piece, board, new_position, original_position):

        # Unpacking the move positions.
        old_col, old_row = original_position
        new_col, new_row = new_position

        # Finding the king locations.
        for col, rank in enumerate(board):
            for row, item in enumerate(rank):
                if isinstance(item, King) and item.color == WHITE:
                    white_king = (col, row)
                    w_king = item
                elif isinstance(item, King) and item.color == BLACK:
                    black_king = (col, row)
                    b_king = item

        # Check if the king is currently in check.
        game.in_check(board, white_king, black_king, w_king, b_king)

        # If king is in check when castling, disallow castling and reset attributes
        if piece.in_check == True:
            piece.in_check = False
            piece.castling = False
            return False

        # If castling in positive x.
        if new_col - old_col > 0:

            # Update the board to move the king one square in positive x.
            # Checking that the king cannot castle through check.
            board[old_col][old_row] = []
            board[old_col + 1][old_row] = piece
            white_king = (old_col + 1, old_row)
            
            
            # Checking if the king is in check.
            game.in_check(board, white_king, black_king, w_king, b_king)

            # If the king is in check, reset the board and king attributes.
            if piece.in_check == True:
                board = self.reset_castling(piece, board, new_col, new_row, old_col, old_row)
                return False

            # Update the board to move the king two squares in positive x.
            board[old_col + 1][old_row] = []
            board[old_col + 2][old_row] = piece
            white_king = (old_col + 2, old_row)

            # Checking if the king is in check.
            game.in_check(board, white_king, black_king, w_king, b_king)

            # If the king is in check, reset the board and king attributes.
            if piece.in_check == True:
                board = self.reset_castling(piece, board, new_col, new_row, old_col, old_row)
                return False

            # Update the board with rook move if castling is allowed.
            right_rook = board[old_col + 3][old_row]
            board[old_col + 3][old_row] = []
            board[old_col + 1][old_row] = right_rook

            # Update the pieces attributes
            piece.move(new_position)
            right_rook.move((old_col + 1, old_row))

            # Draw the rook move on the screen. 
            screen.update_move(board, right_rook, (old_col + 3, old_row))
        return True

    def reset_castling(self, piece, board, new_col, new_row, old_col, old_row):
        piece.in_check = False
        piece.castling = False
        board[old_col][old_row] = piece
        board[new_col][new_row] = []
        board[old_col + 1][old_row] = []
        board[old_col + 2][old_row] = []

        return board