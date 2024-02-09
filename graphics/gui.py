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
        """
        Iterates over a list of points and fills a checkered pattern

        Args:
            point_list (list): List of points corresponding to the location of squares.
            color1 (RGB): First color to draw.
            color2 (RGB): Second color to draw.
        """

        num_cols = len(point_list[0])
        num_rows = len(point_list)
        square_width = self.width // num_cols
        square_height = self.height // num_rows
        
        # Iterates over the list of points and fills in the checkered pattern.
        for row in range(num_rows):
            for col, point in enumerate(point_list[row]):
                fill_color = color1 if (row + col) % 2 == 0 else color2
                self.win.fill(fill_color, (point[0], point[1],
                                            square_width, square_height))

        pygame.display.update()

    def draw_pieces(self, board):
        """
        Loops through the chessboard, finds the pieces, centers and displays the pieces.

        Args:
            board (list): The chessboard as a 2D list
        """
        
        # Gets the size of the board in x and y.
        num_cols = len(board[0])
        num_rows = len(board)

        # Loops through the board, finds the pieces, centers and displays the pieces
        for row in board:
            for piece in row:
                if isinstance(piece, Piece):
                    img = pygame.image.load(piece.img)
                    img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
                    img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
                    x_pos = piece.x * WIDTH // num_cols + img_offset_x
                    y_pos = piece.y * HEIGHT // num_rows + img_offset_y
                    self.win.blit(img, (x_pos, y_pos))

        pygame.display.update()

    def update_move(self, board, piece, original_position, color1, color2):
        # Gets the size of the board in x and y.
        num_cols = len(board[0])
        num_rows = len(board)
        square_width = self.width // num_cols
        square_height = self.height // num_rows
        col, row = original_position

        fill_color = color1 if (col + row) % 2 == 0 else color2
        self.win.fill(fill_color, (col * 100, row * 100,
                                            square_width, square_height))
        
        fill_color = color1 if (piece.x + piece.y) % 2 == 0 else color2
        self.win.fill(fill_color, (piece.x * square_width, piece.y * square_height,
                                            square_width, square_height))

        img = pygame.image.load(piece.img)
        img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
        img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
        x_pos = piece.x * WIDTH // num_cols + img_offset_x
        y_pos = piece.y * HEIGHT // num_rows + img_offset_y
        self.win.blit(img, (x_pos, y_pos))
        pygame.display.update()
