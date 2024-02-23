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
            position1 (tuple): (x, y).
            position2 (tuple): (x, y).

        Returns:
            list: List of tuples containing x and y values.
        """
        new_col, new_row = position1
        old_col, old_row = position2
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
            y_points = [y for y in range(old_row - 1, new_row, -1)]

        
        return list(zip(x_points, y_points))
    
    def piece_in_path(self, chessboard, new_position, original_position):
        
        piece_path = self.find_path_points(new_position, original_position)
        
        for point in piece_path:
            if chessboard.board[point[0]][point[1]] != []:
                return True
            
        return False
    
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
                    if (piece.color == BLACK and piece.is_valid_move(white_king_pos, original_position) == True
                        and self.piece_in_path(chessboard, white_king_pos, original_position) == False
                        and self.can_capture(chessboard, white_king_pos, original_position) == True):
                        print("white in check")
                        self.check_list.append(piece)
                        white_king_object.in_check = True

                    # Trying to move all white pieces to the black king.
                    elif (piece.color == WHITE and piece.is_valid_move(black_king_pos, original_position) == True
                        and self.piece_in_path(chessboard, black_king_pos, original_position) == False
                        and self.can_capture(chessboard, black_king_pos, original_position) == True):
                        black_king_object.in_check = True
                        self.check_list.append(piece)
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
        self.move_list.append((self.move_counter, rook, (new_rook_col, new_row), (rook_col, old_row), []))
        
        # Update the pieces attributes
        piece.move(new_position)
        rook.move((new_col + col_dir_factor * -1, old_row))

        # Draw the rook move on the screen. 
        screen.update_move(chessboard, rook, [], (new_rook_col, new_row), (rook_col, old_row))
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
    
    def results_in_check(self, piece, chessboard):
        """
        Checks if the king that belongs to the piece trying to move is in check.

        Args:
            piece (object): Piece being moved.
            chessboard (list): Chessboard as a 2D list.

        Returns:
            bool: Returns True if the move results in check, False otherwise.
        """

        # Checking if the kings are in check and updating their attribute.
        white_king, black_king = self.in_check(chessboard)

        if white_king.in_check == True and piece.color == WHITE:
            black_king.in_check = False
            return True
        
        elif black_king.in_check == True and piece.color == BLACK:
            white_king.in_check = False
            return True
        
        return False
    
    def all_king_moves(self, king):
        """
        Creates a list of points around the king. This list represents
        moves that the king can possibly make.

        Args:
            king (object): Chess piece, King.

        Returns:
            list: List of points around the king.
        """
        
        cols = [-1, 0, 1]
        rows = [-1, 0, 1]
        king_move_list = [(king.x + col, king.y + row ) for col in cols for row in rows]
        king_move_list.remove((king.x, king.y))
    
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
        king_move_list = self.all_king_moves(king)
        
        # Iterates through the list of points and tries to move the king.
        for point in king_move_list:
            
            # Checks if the king move is valid.
            if (king.valid_move(point, (king.x, king.y))
                and self.can_capture(chessboard, point, (king.x, king.y))):
                
                # Updates the board with the new king move.
                captured_piece = chessboard.update_board(king, point, (king.x, king.y))
                
                # Checks if the new king move results in check.
                if not self.results_in_check(king, chessboard):
                    chessboard.reset_board(king, point, (king.x, king.y), captured_piece)
                    return True
                
                # Resets the board after every iteration.
                chessboard.reset_board(king, point, (king.x, king.y), captured_piece)
            
        return False
            
    def piece_can_block(self, chessboard, king):
        """
        Checks if a piece can block check,

        Args:
            chessboard (list): Chessboard as a 2D list.
            king (object): King in check.

        Returns:
            bool: Returns True if a piece can block check, False otherwise.
        """

        # Getting the piece giving check.
        check_piece = self.check_list[0]
        
        # Getting the path in between the piece giving check and the king.
        check_path = self.find_path_points((check_piece.col, check_piece.row), (king.x, king.y))
        
        # Iterates over the board to check if any pieces can block the check.
        for rank in chessboard.board:
            for piece in rank:
                if piece != [] and not isinstance(piece, King) and piece.color == king.color:
                    for point in check_path:
                        if (piece.is_valid_move(point, (piece.col, piece.row))
                        and not self.piece_in_path(chessboard, point, (piece.col, piece.row))
                        and self.can_capture(chessboard, point,(piece.col, piece.row))):
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
                and self.can_capture(chessboard, (check_piece.col, check_piece.row), (piece.col, piece.row))):
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
    
    def select_promotion(self, pos, chessboard, piece, player):
        if piece.color == WHITE:
            step = [0, 1, 2, 3]
        else:
            step = [0, -1, -2, -3]

        for num in step:
            if player.click_square(pos, chessboard, (piece.col, piece.row + num)):
                if num == 0:
                    return Queen(piece.col, piece.row, piece.color)
                elif num in [-1, 1]:
                    return Rook(piece.col, piece.row, piece.color)
                elif num in [-2, 2]:
                    return Bishop(piece.col, piece.row, piece.color)
                elif num in [-3, 3]:
                    return Knight(piece.col, piece.row, piece.color)