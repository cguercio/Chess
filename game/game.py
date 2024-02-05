from pieces import *



class Game:
    
    # Checks if the move is blocked by another piece.
    def check_move(self, board, piece, old_peice_x, old_peice_y):
        x_list = []
        y_list = []
        num_points = max(abs(piece.x - old_peice_x), abs(piece.y - old_peice_y))

        # Builds a list of x points in between the original piece position
        # and the new piece position.
        if piece.x - old_peice_x == 0:
            x_list = [piece.x for _ in range(1, num_points, 1)]
        elif piece.x - old_peice_x > 0:
            x_list = [x for x in range(old_peice_x + 1, piece.x, 1)]
        else:
            x_list = [x for x in range(piece.x + 1, old_peice_x, 1)]

        # Builds a list of y points in between the original piece position
        # and the new piece position.
        if piece.y - old_peice_y == 0:
            y_list = [piece.y for _ in range(1, num_points, 1)]
        elif piece.y - old_peice_y > 0:
            y_list = [y for y in range(old_peice_y + 1, piece.y, 1)]
        else:
            y_list = [y for y in range(piece.y + 1, old_peice_y, 1)]

        # Combines the x and y lists into a list of points.
        piece_path = list(zip(x_list, y_list))

        # Checks if there is a piece in the move path.
        for point in piece_path:
            if board[point[0]][point[1]] != []:
                piece.x = old_peice_x
                piece.y = old_peice_y
                return False
            else:
                pass
        
        return True




        
        
