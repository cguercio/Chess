from pieces import *
from constants import *

class Game:
    move_list = []
    check_list = []
    move_counter = 0
    
    def update_move_list(self, move, current_piece, old_square, new_square, old_piece):
        current_move = {'move_number': move, 'current_piece': current_piece, 'old_square': old_square, 'new_square': new_square, 'old_piece': old_piece}
        self.move_list.append(current_move)
    
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
    
    def can_capture(self, piece, board, old_square, new_square):
        """
        Check for a valid capture.

        Args:
            board (list): 2D list representing the board.
            old_square (tuple): Original position of the piece.
            new_square (tuple): Position to which the piece is being moved.

        Returns:
            bool: False if the capture is not valid, True otherwise.
        """
        # Unpacking position tuple.
        new_col, new_row = new_square
        
        # Defining helper variables.
        piece_at_new_position = isinstance(board[new_col][new_row], Piece)
        
        # Checks if a piece is trying to capture 
        # and the piece being captures is not the same color.
        if piece_at_new_position:
            are_same_color = board[new_col][new_row].color == piece.color

            if are_same_color:
                return False
        
        # Calls pawn capture logic if piece is a pawn.
        if isinstance(piece, Pawn):
            return self.pawn_can_capture(piece, board, old_square, new_square)
        
        
        return True
        
    def pawn_can_capture(self, piece, board, old_square, new_square):
        """
        Checks for valid pawn capture.

        Args:
            board (list): 2D list representing the board.
            old_square (tuple): Original position of the piece.
            new_square (tuple): Position to which the piece is being moved.

        Returns:
            bool: False if the capture is not valid, True otherwise.
        """

        # Unpacking position tuples.
        old_col, old_row = old_square
        new_col, new_row = new_square
        
        # Defining helper variables.
        piece_in_front_of_pawn = board[new_col][new_row] != []
        pawn_moving_forward = new_col == old_col
        square_is_empty = board[new_col][new_row] == []
        pawn_is_capturing = new_col != old_col
        
        # Check if the pawn is trying to En Passant.
        if pawn_is_capturing and self.can_enpassant(piece, new_square) == True:
            piece.enpassant = True
            return True
        
        # Check if piece is in front of moving pawn, disallowing movement or capture.
        if piece_in_front_of_pawn and pawn_moving_forward:
            return False
        
        # Checks if pawn tries move to capture square but there is
        # no piece to capture, disallow capture or movement.
        elif square_is_empty and pawn_is_capturing:
            return False
        
        return True
    
    def can_enpassant(self, piece, new_square):
        """
        Check if the pawn can perform En Passant.

        Args:
            piece (object): Pawn being moved.

        Returns:
            bool: False if En Passant is not valid, True if it is valid.
        """
        
        # Checks if the move is the first move on which En Passant can
        # never be performed.
        if len(self.move_list) == 0:
            return False
        
        # Unpacking the move list dictionary.
        last_move = self.move_list[-1]
        last_move_piece = last_move['current_piece']
        old_col, old_row = last_move['old_square']
        new_col, new_row = last_move['new_square']
        
        # Defining helper variables.
        white_enpassant_row = 3
        black_enpassant_row = 4
        last_move_is_not_pawn = not isinstance(last_move_piece, Pawn)
        did_not_move_two_squares = abs(new_row - old_row) != 2
        not_adjacent_to_current_pawn = new_col not in [piece.col - 1, piece.col + 1]
        not_capturing_previous_pawn = new_square[0] != new_col
        
        # Check that the pawn is on the En Passant square.
        if piece.color == WHITE and piece.row != white_enpassant_row:
            return False   
        elif piece.color == BLACK and piece.row != black_enpassant_row:
            return False
            
        # Check is the last move was a pawn move.
        if last_move_is_not_pawn:
            return False
        
        # Check if last pawn move was 2 squares.
        if did_not_move_two_squares:
            return False
        
        # Check if last pawn was adjacent to the current pawn.
        if not_adjacent_to_current_pawn:
            return False
        
        # Check if the current pawn is only capturing on the same column as
        # the previous pawn move.
        if not_capturing_previous_pawn:
            return False

        return True
            
                
    def is_valid_move(self, piece, board, old_square, new_square):
        """
        Checks if the move is valid.

        Args:
            piece (object): Piece being moved.
            board (list): 2D list representing the board.
            old_square (tuple): Starting square of the piece.
            new_square (tuple): Square to which the piece is being moved.

        Returns:
            bool: True if move is valid, False otherwise.
        """
        
        piece_move_not_valid = piece.is_valid_move(new_square, old_square) == False
        
        if piece_move_not_valid:
            return False
        
        path_is_blocked = self.piece_in_path(board, old_square, new_square) == True
        
        if path_is_blocked:
            return False
        
        capture_not_valid = self.can_capture(piece, board, old_square, new_square) == False
        
        if capture_not_valid:
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
    
    def get_piece_by_color(self, board, color):
        """
        Gets a list of the pieces on the board given a color.

        Args:
            board (list): 2D list representing the board.
            color (rgb): WHITE or BLACK.

        Returns:
            list: List of pieces on the board of specified color.
        """
        
        # Forcing the color to be either white or black.
        assert color in [WHITE, BLACK]
        
        # Initiating the lists.
        pieces = []
        
        # Iterates over the board and builds piece lists.
        for rank in board:
            for piece in rank:
                if piece != [] and piece.color == color:
                    pieces.append(piece)
                    
                        
        return pieces
    
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
        white_pieces = self.get_piece_by_color(board, WHITE)
        black_pieces = self.get_piece_by_color(board, BLACK)
        
        # Resetting in_check attribute before looking for checks.
        white_king_object.in_check = False
        black_king_object.in_check = False
        
        # Loop through the black piece list.
        for piece in black_pieces:
            
            # Setting the position of the piece.
            piece_position = (piece.col, piece.row)
            
            # Check if a piece can capture the king.
            if self.is_valid_move(piece, board, piece_position, white_king_pos):
                self.check_list.append(piece)
                white_king_object.in_check = True
                print("white in check")
        
        # Loop through the black piece list.        
        for piece in white_pieces:
            
            # Setting the position of the piece.
            piece_position = (piece.col, piece.row)
            
            # Check if a piece can capture the king.
            if self.is_valid_move(piece, board, piece_position, black_king_pos):
                self.check_list.append(piece)
                black_king_object.in_check = True 
                print("black in check")

        return white_king_object, black_king_object

    def can_castle(self, screen, king, chessboard, old_square, new_square):
        """
        Checks if the king is allowed to castle.

        Args:
            screen (object): Screen object.
            king (object): King object that is castling.
            chessboard (object): Board object.
            old_square (tuple): Original position of the king.
            new_square (tuple): Castling position of king.

        Returns:
            bool: False if king is not allowed to castle, True otherwise.
        """
        
        old_col, old_row = old_square
        new_col, new_row = new_square
        col_diff = new_col - old_col
        
        # Check if the king is currently in check.
        self.in_check(chessboard.board)

        # If king is in check when castling, disallow castling and reset attributes
        if king.in_check == True:
            king.in_check = False
            king.castling = False
            return False
        
        # Finds the appropriate rook object depending on which direction the user castled.
        rook_col = 0 if col_diff < 0 else chessboard.cols - 1
        rook = chessboard.board[rook_col][old_row]
        
        if self.piece_in_path(chessboard.board, (rook.col, rook.row), (king.col, king.row)):
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
            castling_new_square = (next_col, old_row)
            previous_square = (previous_col, old_row)
            
            # Updates the board with the new moves.
            chessboard.update_board(king, previous_square, castling_new_square)
            
            # Checking to see if the new square is in check.
            self.in_check(chessboard.board)
                
            # Checks if the king is in check.
            if king.in_check == True:
                chessboard.reset_castling(king, old_square, castling_new_square, index)
                return False 
        
        castled_queenside = left_castle == -1
        
        # If the king castles queenside update an extra square.
        if castled_queenside:
            chessboard.update_board(king, (next_col, old_row), (new_col, new_row))

        # Checks for a previous rook move.
        if rook.has_moved == True:
            chessboard.reset_castling(king, old_square, new_square, index)
            return False
            
        # Update the board with rook move if castling is allowed.
        new_rook_col = new_col + (col_dir_factor * -1)
        chessboard.update_board(rook, (rook_col, old_row), (new_rook_col, new_row))
        
        # Updates the move list with the rook move.
        self.update_move_list(self.move_counter, rook, (rook_col, old_row), (new_rook_col, new_row), [])
        
        # Update the piece moves.
        king.move(new_square)
        rook.move((new_rook_col, old_row))

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
                        and self.can_capture(king, chessboard.board, king_position, position)) == True
            
            # Checks if the king move is valid.
            if move_is_valid:
                
                # Updates the board with the new king move.
                captured_piece = chessboard.update_board(king, king_position, position)
                
                king_not_in_check = self.results_in_check(king, chessboard.board) == False
                
                # Checks if the new king move results in check.
                if king_not_in_check:
                    chessboard.reset_board(king, king_position, position, captured_piece)
                    return True
                
                # Resets the board after every iteration.
                chessboard.reset_board(king, king_position, position, captured_piece)
            
        return False
            
    def piece_can_block(self, board, king):
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
        
        # Getting the pieces that have the same color as the king.
        pieces = self.get_piece_by_color(board, king.color)
        
        # Iterates through the list of pieces.
        for piece in pieces:
            # Check that the piece is not a king.
            if not isinstance(piece, King):
                
                # Iterates over every square in the path of check.
                for square in check_path:
                    piece_position = (piece.col, piece.row)
                    
                    # Checks if a piece moving in the path of the check is valid.
                    if self.is_valid_move(piece, board, piece_position, square) == True:
                        return True
                        
        return False
    
    def can_capture_check_piece(self, board, king): ###### not detecting checkmate after change here
        """
        Checks if a piece can capture the piece giving check.

        Args:
            chessboard (list): Chessboard as a 2D list.
            king (object): King in check.

        Returns:
            bool: Returns True if piece can be captured, False otherwise.
        """
        # Getting the piece giving check.
        piece_giving_check = self.check_list[0]
        piece_giving_check_position = (piece_giving_check.col, piece_giving_check.row)
        
        # Getting all pieces that have the same color as the king in check.
        pieces = self.get_piece_by_color(board, king.color)
        
        # Loop through the pieces and try to move them to the piece giving check.
        for piece in pieces:
            # Check that the piece is not a king.
            if not isinstance(piece, King):
                
                # Checks if a piece can capture the piece giving check.
                if self.is_valid_move(piece, board, (piece.col, piece.row), piece_giving_check_position):
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
        
        # Defining helper variables.
        is_double_check = len(self.check_list) > 1
        king_cant_move = self.king_can_move(chessboard, king) == False
        piece_cant_block = self.piece_can_block(chessboard.board, king) == False
        cant_capture_check_piece = self.can_capture_check_piece(chessboard.board, king) == False
        
        # If king is in double check, only king move is checked.
        if is_double_check and king_cant_move:
            return True
        
        # If king is not in double check, check if king can move,
        # if piece can block, and piece giving check can be captured.
        elif (king_cant_move
                and piece_cant_block
                and cant_capture_check_piece):
            return True
        
        return False