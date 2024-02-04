from pieces import *



class Game:
    
    def check_move(self, board, piece, old_peice_x, old_peice_y):
        checkx = []
        checky = []

        for row in range(abs(piece.x - old_peice_x)):
            checkx.append(old_peice_x + row)
        for col in range(abs(piece.y - old_peice_y)):
            checky.append(old_peice_y + col)
        try:
            for i, j in checkx, checky:
                if board[i][j] == []:
                    pass
                else:
                    return True
        except:
            print("False")
            return False
                    