import pygame
from constants import *
from pieces import *
pygame.init()
pygame.font.init()

class Screen:

    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))


    # Method takes in a list of lists of points and uses it to draw a checkered pattern.
    # This method works with any size grid
    def draw_squares(self, point_list, color1, color2):
        num_cols = len(point_list[0]) # Gets the number of cols by geting the length of the first list
        num_rows = len(point_list) # Gets the number of rows by getting the number of lists

        # Iterates over every other row starting at 1st row.
        for row in range(0,num_rows,2):
            for col in range(num_cols):

                # If col row is even fill with color 1.
                if col % 2 == 0:
                    point = (point_list[row][col]) # This is here to access the elements in the points using idexing.
                    self.win.fill(color1, (point[0], point[1],
                                            self.width // num_cols, self.height // num_rows))
                else: # If col row is odd fill with color 2.
                    point = (point_list[row][col]) # This is here to access the elements in the points using idexing.
                    self.win.fill(color2, (point[0], point[1],
                                             self.width // num_cols, self.height // num_rows))
        
        # Iterates over every other row starting at 2nd row.
        for row in range(1,num_rows,2):
            for col in range(num_cols):
                if col % 2 == 0: # If col row is even fill with color 1.
                    point = (point_list[row][col]) # This is here to access the elements in the points using idexing.
                    self.win.fill(color2, (point[0], point[1],
                                             self.width // num_cols, self.height // num_rows))
                else:# If col row is odd fill with color 2.
                    point = (point_list[row][col]) # This is here to access the elements in the points using idexing.
                    self.win.fill(color1, (point[0], point[1],
                                             self.width // num_cols, self.height // num_rows))
        
        pygame.display.update()

    def draw_pieces(self, board):
        num_cols = len(board[0]) # Gets the number of cols by geting the length of the first list
        num_rows = len(board) # Gets the number of rows by getting the number of lists
        img = pygame.image.load('D:\Coding\Cloned Repositories\Chess\graphics\\b_rook_png_shadow_100px.png')
        for row in board:
            for piece in row:
                if isinstance(piece, Piece):
                    self.win.blit(img, (piece.x * 100 + 7, piece.y * 100 + 2))

        pygame.display.update()