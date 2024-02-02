class Board:

    def __init__(self, x_squares, y_squares, color1, color2):
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.color1 = color1
        self.color2 = color2

    def squares(self):
        point_list = [WIDTH]

        return point_list