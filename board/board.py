from constants import *

class Board:

    def __init__(self, x_squares, y_squares, color1, color2):
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.color1 = color1
        self.color2 = color2
        self.board = ['' for _ in range(x_squares) for _ in range(y_squares)]





    def squares(self):

        #  x_list = [x for x in range(0, WIDTH, WIDTH // self.x_squares)]
        #  y_list = [y for y in range(0, HEIGHT, HEIGHT // self.x_squares)]
        #  rect_list = [(x, y, 100, 100) for x in x_list for y in y_list]
        #  print(rect_list)

        for _ in self.board:
            point_list = [[(x, y) for x in range(0, WIDTH, WIDTH // self.x_squares)]
            for y in range(0, HEIGHT, HEIGHT // self.x_squares)]
        print(point_list)
        print(point_list[0])

        return point_list
        