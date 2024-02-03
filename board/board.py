from constants import *

class Board:

    def __init__(self, x_squares, y_squares):
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.board = ['' for _ in range(x_squares) for _ in range(y_squares)]

    # Method builds a list of lists of points for squares
    def squares(self):

        for _ in self.board:
            point_list = [[(x, y) for x in range(0, WIDTH, WIDTH // self.x_squares)]
            for y in range(0, HEIGHT, HEIGHT // self.y_squares)]
        return point_list
        