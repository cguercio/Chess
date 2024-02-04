from constants import *
from utils import *

class Board:

    def __init__(self, x_squares, y_squares):
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.board = [[[] for _ in range(x_squares)] for _ in range(y_squares)]

    # Method builds a list of lists of points for squares to be drawn
    def squares(self):

        for _ in self.board:
            square_list = [[(x, y) for x in range(0, WIDTH, WIDTH // self.x_squares)]
            for y in range(0, HEIGHT, HEIGHT // self.y_squares)]
        return square_list
    
    def place_piece(self, piece):
        self.board[piece.x][piece.y] = piece

    def update_piece(self, piece, x, y):
        self.board[x][y] = []
        self.board[piece.x][piece.y] = piece
