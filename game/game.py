from pieces import *
from constants import *
from player import *
from graphics import *




class Game:
    
    # Checks if the move is blocked by another piece.
    def piece_path(self, chessboard, new_position, original_position):
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
            if chessboard.board[point[0]][point[1]] != []:
                return False

        return True
    
    def can_capture(self, chessboard, new_position, original_position):
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
        if (chessboard.board[new_col][new_row] != []
            and chessboard.board[new_col][new_row].color == chessboard.board[old_col][old_row].color):
            return False
        
        # Calls pawn capture logic if piece is a pawn.
        if isinstance(chessboard.board[old_col][old_row], Pawn):
            return self.pawn_can_capture(chessboard, new_position, original_position)
        
        return True
        
    def pawn_can_capture(self, chessboard, new_position, original_position):
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
        if (chessboard.board[new_col][new_row] and new_col == old_col):
            return False
        
        # Checks if pawn tries move to capture square but there is
        # no piece to capture, disallow capture or movement.
        elif not chessboard.board[new_col][new_row] and new_col != old_col:
            return False
        
        # self.update_capture(board, new_col, new_row)        
        return True
    
    def in_check(self, chessboard):
        """
        Checks both kings for check and sets check
        attribute to True if necessary.

        Args:
            board (list): Chess board as a 2D list.
            w_king (object): White king.
            b_king (object): Black king.
        """

        # Finds the location of the kings on the temp board.
        white_king_pos, white_king_object, black_king_pos, black_king_object = self.find_kings(chessboard) 
        white_king_object.in_check = False
        black_king_object.in_check = False
        
        # Looping thought piece objects.
        for col, rank in enumerate(chessboard.board):
            for row, piece in enumerate(rank):
                if piece != []:
                    original_position = (col, row)
                    # Trying to move all black pieces to the white king.
                    if (piece.color == BLACK and piece.valid_move(white_king_pos, original_position) == True
                        and self.piece_path(chessboard, white_king_pos, original_position) == True
                        and self.can_capture(chessboard, white_king_pos, original_position) == True):
                        print("white in check")
                        white_king_object.in_check = True

                    # Trying to move all white pieces to the black king.
                    elif (piece.color == WHITE and piece.valid_move(black_king_pos, original_position) == True
                        and self.piece_path(chessboard, black_king_pos, original_position) == True
                        and self.can_capture(chessboard, black_king_pos, original_position) == True):
                        black_king_object.in_check = True
                        print("black in check")

        return white_king_object, black_king_object

    def castling(self, screen, piece, chessboard, new_position, original_position):

        # Unpacking the move positions.
        num_cols = len(chessboard.board[0]) # Gets the number of cols by getting the length of the first list
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        row_diff = new_row - old_row
        col_diff = new_col - old_col
        
        # Check if the king is currently in check.
        self.in_check(chessboard)

        # If king is in check when castling, disallow castling and reset attributes
        if piece.in_check == True:
            piece.in_check = False
            piece.castling = False
            return False, chessboard
        
        # Column direction factor determines the direction of the move.
        # This is used for the range start and step of the iteration.
        col_dir_factor = -1 if col_diff < 0 else 1
        
        # left_castle is -1 if if castling queen's side. It provides an extra iteration
        # in the negative direction when checking if the king is castling through check.
        left_castle = -1 if col_diff < 0 else 0
        
        # Naming range inputs for readability.
        range_start = col_dir_factor
        range_end = col_diff + col_dir_factor + left_castle
        range_step = col_dir_factor
        
        # Loops through the squares required to castle and checks for pieces controlling those squares.
        for i in range(range_start, range_end, range_step):
            
            # Calculates the int for the previous and next squares.
            previous_col = old_col + i - col_dir_factor
            next_col = old_col + i
            
            # Updates the board with the new moves.
            
            chessboard.update_board(piece, (next_col, old_row), (previous_col, old_row))
            
            # Checking to see if the new square is in check.
            self.in_check(chessboard)
                
            # Checks if the king is in check.
            if piece.in_check == True:
                chessboard.reset_castling(piece, new_position, original_position, i)
                return False, chessboard
        
        # If the king castles in negative x an extra square is reset.
        if left_castle == -1:
            chessboard.update_board(piece, (new_col, new_row), (next_col, old_row))

        # Finds the appropriate rook object depending on which direction the user castled.
        rook_col = 0 if col_diff < 0 else num_cols - 1
        rook = chessboard.board[rook_col][old_row]
        
        # Update the board with rook move if castling is allowed.
        new_rook_col = new_col + col_dir_factor * -1
        chessboard.update_board(rook, (new_rook_col, new_row), (rook_col, old_row))
        
        # Update the pieces attributes
        piece.move(new_position)
        rook.move((new_col + col_dir_factor * -1, old_row))

        # Draw the rook move on the screen. 
        screen.update_move(chessboard, rook, (rook_col, old_row))
        piece.has_moved = True

        return True, chessboard

    def find_kings(self, chessboard):
        """
        Find the location of the kings on any given board.

        Args:
            board (list): Chessboard as a 2D list.

        Returns:
            tuple, object: Returns king locations and objects.
        """
        
        for col, rank in enumerate(chessboard.board):
            for row, item in enumerate(rank):
                if isinstance(item, King) and item.color == WHITE:
                    white_king_pos = (col, row)
                    white_king_object = item
                elif isinstance(item, King) and item.color == BLACK:
                    black_king_pos = (col, row)
                    black_king_object = item
                    
        return white_king_pos, white_king_object, black_king_pos, black_king_object
    