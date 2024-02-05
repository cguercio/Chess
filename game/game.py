from pieces import *
from constants import *



class Game:
    
    # Checks if the move is blocked by another piece.
    def check_move(self, board, piece, original_position):
        num_points = max(abs(piece.x - original_position[0]), abs(piece.y - original_position[1]))

        # Builds a list of x points in between the original piece position
        # and the new piece position.
        if piece.x - original_position[0] == 0:
            x_list = [piece.x for _ in range(1, num_points, 1)]
        elif piece.x - original_position[0] > 0:
            x_list = [x for x in range(original_position[0] + 1, piece.x, 1)]
        else:
            # If negative in x, we need to reverse the y list
            x_list = reversed([x for x in range(piece.x + 1, original_position[0], 1)])

        # Builds a list of y points in between the original piece position
        # and the new piece position.
        if piece.y - original_position[1] == 0:
            y_list = [piece.y for _ in range(1, num_points, 1)]
        elif piece.y - original_position[1] > 0:
            y_list = [y for y in range(original_position[1] + 1, piece.y, 1)]
        else:
            # If negative in y, we need to reverse the y list
            y_list = reversed([y for y in range(piece.y + 1, original_position[1], 1)])

        # Combines the x and y lists into a list of points.
        piece_path = list(zip(x_list, y_list))

        # Checks if there is a piece in the move path.
        for point in piece_path:
            if board[point[0]][point[1]] != []:
                piece.x = original_position[0]
                piece.y = original_position[1]
                return False

        
        # Checks if it is a valid capture.
        if self.check_capture(board, piece, original_position) == True:
            return True
        else:
            piece.x = original_position[0]
            piece.y = original_position[1]
            return False
    
    def check_capture(self, board, piece, original_position):

        # Checks if the piece tries to capture its own color.
        if (board[piece.x][piece.y] != []
            and board[piece.x][piece.y].color == piece.color):
                piece.x = original_position[0]
                piece.y = original_position[1]
                return False
        
        # Governs the pawn capture logic.
        if isinstance(piece, Pawn):

            # Checks for piece in front of pawn and doesnt allow it to move.
            if (board[piece.x][piece.y] != [] and piece.x - original_position[0] == 0):
                piece.x = original_position[0]
                piece.y = original_position[1]
                return False

            # Checks for piece on pawn capture square
            elif (board[piece.x][piece.y] != []
                and piece.x - original_position[0] != 0):
                return True
                
            # Checks if the pawn tries to capture, but there is no piece.
            elif piece.x - original_position[0] != 0:
                  piece.x = original_position[0]
                  piece.y = original_position[1]
                  return False
            else: 
                return True

        else:
            return True    
        




        
        
