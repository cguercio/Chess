from pieces import *
from constants import *
from player import *




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
                        
        # Looping thought piece objects.
        for col, rank in enumerate(board):
            for row, piece in enumerate(rank):
                if piece != []:
                    original_position = (col, row)
                    # Trying to move all black pieces to the white king.
                    if (piece.color == BLACK and piece.valid_move(white_king, original_position) == True
                        and self.piece_path(board, white_king, original_position) == True
                        and self.can_capture(board, white_king, original_position) == True):
                        w_king.check = True
                        print("White in check.")

                    elif (piece.color == WHITE and piece.valid_move(black_king, original_position) == True
                        and self.piece_path(board, black_king, original_position) == True
                        and self.can_capture(board, black_king, original_position) == True):
                        b_king.check = True
                        print("Black in check.")

            # Trying to move all white pieces to the black king.0
            
        
    def update_capture(self, player):
        """
        Tries to sets the object's is_captured attribute to true.

        Args:
            board (list): Chess board represented as a 2D list.
            new_col (int): New piece column
            new_row (int): New piece row.
        """
        piece_locations = [(piece.x, piece.y) for piece in Piece.instances]

        for index, item in enumerate(piece_locations):
            if piece_locations.count(item) > 1:
                if Piece.instances[index].color != player.color:
                    Piece.instances[index].is_captured = True
                    Piece.instances[index].check_capture()

                    
                
            
                    
        # try:
        #     board[new_col][new_row].is_captured = True
        #     board[new_col][new_row].check_capture()
        # except Exception:
        #     pass
    def get_last_game_state(self, piece_list, board_list):
        
        return piece_list[-1], board_list[-1]

        



        
        
