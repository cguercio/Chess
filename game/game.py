from pieces import *
from constants import *
from player import *
from graphics import *
from utils import *




class Game:
    move_list = []
    check_list = []
    move_counter = 0
    
    # Checks if the move is blocked by another piece.
    def find_path_points(self, position1, position2):
        """
        Builds a list of points in between two locations on the board.

        Args:
            position1 (tuple): Board position: (col, row).
            position2 (tuple): Board position: (col, row).

        Returns:
            list: List of tuples containing board positions in between the pieces.
        """
        
        # Unpacking position tuples.
        col1, row1 = position1
        col2, row2 = position2
        
        # Defining helper variables.
        num_points = max(abs(col1 - col2), abs(row1 - row2))
        num_points_list = range(1, num_points)
        
        # Checks if col position stays the same.
        if col1 == col2:
            # Since col did not change, populate the list with the original column
            # for the number of points needed.
            col_points = [col1 for _ in num_points_list]
        elif col1 > col2:
            # Since col2 is less than col1, iterate forward from col2 to col1.
            # This populates the list in ascending order.
            col_points = [col for col in range(col2 + 1, col1)]
        else:
            # Since col1 is less than col2, iterate backward from col1 to col2.
            # This populates the list in ascending order.
            col_points = [col for col in range(col2 - 1, col1, -1)]

        # Builds a list of y points in between the original piece position
        # and the new piece position.
        if row1 == row2:
            # Since row did not change, populate the list with the original row
            # for the number of points needed.
            row_points = [row1 for _ in num_points_list]
        elif row1 > row2:
            # Since row2 is less than row1, iterate forward from row2 to row1.
            # This populates the list in ascending order.
            row_points = [row for row in range(row2 + 1, row1)]
        else:
            # Since row1 is less than row2, iterate backward from row1 to row2.
            # This populates the list in ascending order.
            row_points = [row for row in range(row2 - 1, row1, -1)]

        # Zips the lists together to create a list of tuples representing
        # the path between two points.
        points_in_path = list(zip(col_points, row_points))
        
        return points_in_path
    
    
    def piece_in_path(self, board, position1, position2):
        """
        Checks if a piece is in the path of two points.

        Args:
            board (list): 2D list representing the board.
            position1 (tuple): Position 1 on the board: (col, row)
            position2 (tuple): Position 2 on the board: (col, row)

        Returns:
            bool: True if there is a piece in the path, False otherwise.
        """

        # Getting the path between the two positions.
        piece_path = self.find_path_points(position1, position2)
        
        # Loops over the positions in the path.
        for point in piece_path:
            
            # Checks for a piece in the position.
            piece_in_position = board[point[0]][point[1]] != []
            
            if piece_in_position:
                return True
            
        return False
    
    def can_capture(self, board, new_position, original_position):
        """
        Check for a valid capture.

        Args:
            board (list): 2D list representing the board.
            new_position (tuple): Position to which the piece is being moved.
            original_position (tuple): Original position of the piece.

        Returns:
            bool: False if the capture is not valid, True otherwise.
        """
        # Unpacking position tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        # Defining helper variables.
        piece = board[old_col][old_row]
        piece_at_new_position = board[new_col][new_row] != []
        
        # Checks if a piece is trying to capture 
        # and the piece being captures is not the same color.
        if piece_at_new_position:
            
            are_same_color = board[new_col][new_row].color == piece.color
            
            if are_same_color:
                return False
        
        # Calls pawn capture logic if piece is a pawn.
        if isinstance(piece, Pawn):
            return self.pawn_can_capture(board, new_position, original_position)
        
        
        return True
        
    def pawn_can_capture(self, board, new_position, original_position):
        """
        Checks for valid pawn capture.

        Args:
            board (list): 2D list representing the board.
            new_position (tuple): Position to which the piece is being moved.
            original_position (tuple): Original position of the piece.

        Returns:
            bool: False if the capture is not valid, True otherwise.
        """

        # Unpacking position tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position
        
        # Defining helper variables.
        piece_in_front_of_pawn = board[new_col][new_row] != []
        pawn_moving_forward = new_col == old_col
        square_is_empty = board[new_col][new_row] == []
        pawn_is_capturing = new_col != old_col
        
        # Check if piece is in front of moving pawn, disallowing movement or capture.
        if piece_in_front_of_pawn and pawn_moving_forward:
            return False
        
        # Checks if pawn tries move to capture square but there is
        # no piece to capture, disallow capture or movement.
        elif square_is_empty and pawn_is_capturing:
            return False
        
        return True

    def find_kings(self, board):
        """
        Find the location of the kings on any given board.

        Args:
            board (list): Chessboard as a 2D list.

        Returns:
            tuple, object: Returns king locations and objects:
            white_king_pos, white_king_object, black_king_pos, black_king_object
        """
        # Iterates over the board to find the black and white kings.
        for col, rank in enumerate(board):
            for row, item in enumerate(rank):
                if isinstance(item, King) and item.color == WHITE:
                    white_king_pos = (col, row)
                    white_king_object = item
                elif isinstance(item, King) and item.color == BLACK:
                    black_king_pos = (col, row)
                    black_king_object = item
                    
        return white_king_pos, white_king_object, black_king_pos, black_king_object
    
    def find_all_pieces(self, board):
        """
        Iterates over a given board and builds lists of pieces.

        Args:
            board (list): 2D list representing the board.

        Returns:
            list: Lists of black and white pieces: white_pieces, black_pieces
        """
        
        # Initiating the lists.
        black_pieces = []
        white_pieces =[]
        
        # Iterates over the board and builds piece lists.
        for rank in board:
            for piece in rank:
                if piece != []:
                    if piece.color == BLACK:
                        black_pieces.append(piece)
                    elif piece.color == WHITE:
                        white_pieces.append(piece)
                        
        return white_pieces, black_pieces
    
    def in_check(self, board):
        """
        Checks if the kings are in check and updates the in_check attribute.

        Args:
            board (list): 2D list representing the board.

        Returns:
            object: King objects: white_king,
        """

        # Getting king objects and locations
        white_king_pos, white_king_object, black_king_pos, black_king_object = self.find_kings(board) 
        
        # Getting white and black piece lists.
        white_pieces, black_pieces = self.find_all_pieces(board)
        
        # Resetting in_check attribute before looking for checks.
        white_king_object.in_check = False
        black_king_object.in_check = False
        
        # Loop through the black piece list.
        for piece in black_pieces:
            
            # Setting the position of the piece.
            original_position = (piece.col, piece.row)
            
            # Check if a piece can capture the king.
            if self.piece_can_capture_king(piece, board, white_king_pos, original_position):
                self.check_list.append(piece)
                white_king_object.in_check = True 
        
        # Loop through the black piece list.        
        for piece in white_pieces:
            
            # Setting the position of the piece.
            original_position = (piece.col, piece.row)
            
            # Check if a piece can capture the king.
            if self.piece_can_capture_king(piece, board, black_king_pos, original_position):
                self.check_list.append(piece)
                black_king_object.in_check = True 

        return white_king_object, black_king_object
    
    def piece_can_capture_king(self, piece, board, king_position, original_position):
        """
        Checks if a piece move to and capture the king.

        Args:
            piece (object): Piece moving to king.
            board (list): 2D list representing the board.
            king_position (tuple): Position of king: (col, row)
            original_position (tuple): Original position of piece: (col, row)

        Returns:
            bool: True if king can be captured, false otherwise.
        """
        
        # Check is piece can move to and capture the king.
        if (piece.is_valid_move(king_position, original_position) == True
            and self.piece_in_path(board, king_position, original_position) == False
            and self.can_capture(board, king_position, original_position) == True):
            return True
        
        return False
    

    def can_castle(self, screen, king, chessboard, new_position, original_position):
        """
        Checks if the king is allowed to castle.

        Args:
            screen (object): Screen object.
            king (object): King object that is castling.
            chessboard (object): Board object.
            new_position (tuple): Castling position of king.
            original_position (tuple): Original position of the king.

        Returns:
            bool: False if king is not allowed to castle, True otherwise.
        """
        
        old_col, old_row = original_position
        new_col, new_row = new_position
        col_diff = new_col - old_col
        
        # Check if the king is currently in check.
        self.in_check(chessboard.board)

        # If king is in check when castling, disallow castling and reset attributes
        if king.in_check == True:
            king.in_check = False
            king.castling = False
            return False 
        
        # Column direction factor determines the direction of the move.
        # This is used for the range start and step of the iteration.
        col_dir_factor = -1 if col_diff < 0 else 1
        
        # left_castle is -1 if castling queen's side. It provides an extra iteration
        # in the negative direction when checking if the king is castling through check.
        left_castle = -1 if col_diff < 0 else 0
        
        # Naming range inputs for readability.
        range_start = col_dir_factor
        range_end = col_diff + col_dir_factor + left_castle
        range_step = col_dir_factor
        castling_index = range(range_start, range_end, range_step)
        
        # Loops through the squares required to castle and checks for pieces controlling those squares.
        # Moves the king one square and then checks for king in check.
        for index in castling_index:
            
            # Calculates the int for the previous and next squares.
            previous_col = old_col + index - col_dir_factor
            next_col = old_col + index
            new_square = (next_col, old_row)
            previous_square = (previous_col, old_row)
            
            # Updates the board with the new moves.
            chessboard.update_board(king, new_square, previous_square)
            
            # Checking to see if the new square is in check.
            self.in_check(chessboard.board)
                
            # Checks if the king is in check.
            if king.in_check == True:
                chessboard.reset_castling(king, new_position, original_position, index)
                return False 
        
        castled_queenside = left_castle == -1
        
        # If the king castles queenside update an extra square.
        if castled_queenside:
            chessboard.update_board(king, (new_col, new_row), (next_col, old_row))

        # Finds the appropriate rook object depending on which direction the user castled.
        rook_col = 0 if col_diff < 0 else chessboard.cols - 1
        rook = chessboard.board[rook_col][old_row]
        
        # Checks for a previous rook move.
        if rook.has_moved == True:
            chessboard.reset_castling(king, new_position, original_position, index)
            return False
        
        # Update the board with rook move if castling is allowed.
        new_rook_col = new_col + col_dir_factor * -1
        chessboard.update_board(rook, (new_rook_col, new_row), (rook_col, old_row))
        
        # Updates the move list with the rook move.
        self.move_list.append((self.move_counter, rook, (new_rook_col, new_row), (rook_col, old_row), []))
        
        # Update the piece moves.
        king.move(new_position)
        rook.move((new_col + col_dir_factor * -1, old_row))

        # Draw the rook move on the screen. 
        screen.update_move(chessboard, rook, [], (new_rook_col, new_row), (rook_col, old_row))
        king.castling = False

        return True
    
    def results_in_check(self, piece, board):
        """
        Checks if the king that belongs to the piece trying to move is in check.

        Args:
            piece (object): Piece being moved.
            chessboard (list): Chessboard as a 2D list.

        Returns:
            bool: Returns True if the move results in check, False otherwise.
        """

        # Checking if the kings are in check and updating their attribute.
        white_king, black_king = self.in_check(board)
        
        white_king_in_check = white_king.in_check == True
        piece_is_white = piece.color == WHITE
        black_king_in_check = black_king.in_check == True
        piece_is_black = piece.color == BLACK
        
        # Check if white is moving and white's king is in check.
        if white_king_in_check and piece_is_white:
            black_king.in_check = False
            return True
        
        # Check if black is moving and black's king is in check.
        elif black_king_in_check and piece_is_black:
            white_king.in_check = False
            return True
        
        return False
    
    def get_all_king_moves(self, king):
        """
        Creates a list of points around the king. This list represents
        moves that the king can possibly make.

        Args:
            king (object): Chess piece, King.

        Returns:
            list: List of points around the king.
        """
        # Lists used to add to king position.
        cols = [-1, 0, 1]
        rows = [-1, 0, 1]
        
        # Builds a list of positions around the king.
        king_move_list = [(king.col + col, king.row + row ) for col in cols for row in rows]
        
        # Removes the current position from the list.
        king_move_list.remove((king.col, king.row))
    
        return king_move_list
    
        
    def king_can_move(self, chessboard, king):
        """
        Checks if the king has any valid moves.

        Args:
            chessboard (list): Chessboard as a 2D list.
            king (object): King to be moved.

        Returns:
            bool: Returns True if the king has a valid move, False otherwise.
        """
        # Getting the list of points around the king.
        king_move_list = self.get_all_king_moves(king)
        king_position = (king.col, king.row)
        
        # Iterates through the list of points and tries to move the king.
        for position in king_move_list:
            
            # True if king can move and king can capture.
            move_is_valid = (king.is_valid_move(position, king_position) == True
                        and self.can_capture(chessboard.board, position, king_position)) == True
            
            # Checks if the king move is valid.
            if move_is_valid:
                
                # Updates the board with the new king move.
                captured_piece = chessboard.update_board(king, position, king_position)
                
                king_not_in_check = self.results_in_check(king, chessboard.board) == False
                
                # Checks if the new king move results in check.
                if king_not_in_check:
                    chessboard.reset_board(king, position, king_position, captured_piece)
                    return True
                
                # Resets the board after every iteration.
                chessboard.reset_board(king, position, king_position, captured_piece)
            
        return False
            
    def piece_can_block(self, chessboard, king): ######## Start here
        """
        Checks if a piece can block check.

        Args:
            chessboard (list): Chessboard as a 2D list.
            king (object): King in check.

        Returns:
            bool: Returns True if a piece can block check, False otherwise.
        """

        # Getting the piece giving check.
        check_piece = self.check_list[0]
        
        # Getting the path in between the piece giving check and the king.
        check_path = self.find_path_points((check_piece.col, check_piece.row), (king.col, king.row))
        
        # Iterates over the board to check if any pieces can block the check.
        for rank in chessboard.board:
            for piece in rank:
                if piece != [] and not isinstance(piece, King) and piece.color == king.color:
                    for point in check_path:
                        if (piece.is_valid_move(point, (piece.col, piece.row))
                        and not self.piece_in_path(chessboard.board, point, (piece.col, piece.row))
                        and self.can_capture(chessboard.board, point,(piece.col, piece.row))):
                            print("not mate")
                            return True
                        
        return False
    
    def can_capture_check_piece(self, chessboard, king):
        """
        Checks if a piece can capture the piece giving check.

        Args:
            chessboard (list): Chessboard as a 2D list.
            king (object): King in check.

        Returns:
            bool: Returns True if piece can be captured.
        """
        # Getting the piece giving check.
        check_piece = self.check_list[0]
        
        # Iterates over the board to check if any pieces can capture the piece giving check.
        for rank in chessboard.board:
            for piece in rank:
                if (piece != [] and not isinstance(piece, King) and piece.color == king.color
                and piece.is_valid_move((check_piece.col, check_piece.row), (piece.col, piece.row))
                and self.piece_in_path(chessboard.board, (check_piece.col, check_piece.row), (piece.col, piece.row)) == False
                and self.can_capture(chessboard.board, (check_piece.col, check_piece.row), (piece.col, piece.row))):
                    return True

        return False
    
    def is_checkmate(self, chessboard, king):
        """
        Checks if checkmate is on the board.

        Args:
            chessboard (list): Chessboard as a 2D list.
            king (object): King in check.

        Returns:
            bool: Returns True if checkmate is on the board, False otherwise.
        """
        
        # If check list has two pieces in it, king is in double check.
        # If king is in double check, only king move is checked.
        if (len(self.check_list) > 1
        and not self.king_can_move(chessboard, king)):
            return True
        elif (not self.king_can_move(chessboard, king)
        and not self.piece_can_block(chessboard, king)
        and not self.can_capture_check_piece(chessboard, king)):
            return True
        
        return False