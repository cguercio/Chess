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

    def draw_pieces(self, chessboard):
        """
        Loops through the chessboard, finds the pieces, centers and displays the pieces.

        Args:
            board (list): The chessboard as a 2D list
        """
        
        # Gets the size of the board in x and y.
        num_cols = len(chessboard.board[0])
        num_rows = len(chessboard.board)

        # Loops through the board, finds the pieces, centers and displays the pieces
        for row in chessboard.board:
            for piece in row:
                if isinstance(piece, Piece):
                    img = pygame.image.load(piece.img)
                    img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
                    img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
                    x_pos = piece.x * WIDTH // num_cols + img_offset_x
                    y_pos = piece.y * HEIGHT // num_rows + img_offset_y
                    self.win.blit(img, (x_pos, y_pos))

        pygame.display.update()

    def update_move(self, chessboard, piece, original_position):
        """
        Clears the starting square, clears the new square,
        displays the piece on the new square.

        Args:
            board (list): Chessboard as a 2D list.
            piece (object): Piece being moved.
            original_position (tuple): Original position of the piece.
        """
        
        
        # Gets the size of the board in x and y.
        num_cols = len(chessboard.board[0])
        num_rows = len(chessboard.board)

        # Getting the height and width of the squares
        square_width = self.width // num_cols
        square_height = self.height // num_rows

        col, row = original_position    

        # Color the piece original square with the correct color.
        fill_color = WHITE if (col + row) % 2 == 0 else GREEN
        self.win.fill(fill_color, (col * square_width, row * square_height,
                                            square_width, square_height))
        
        # Color the new square with the correct color. 
        # This clears the square of any pieces that are on that square.
        fill_color = WHITE if (piece.x + piece.y) % 2 == 0 else GREEN
        self.win.fill(fill_color, (piece.x * square_width, piece.y * square_height,
                                            square_width, square_height))

        # Loads and displays the image of the piece at it's new location.
        img = pygame.image.load(piece.img)
        img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
        img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
        x_pos = piece.x * WIDTH // num_cols + img_offset_x
        y_pos = piece.y * HEIGHT // num_rows + img_offset_y
        self.win.blit(img, (x_pos, y_pos))
        pygame.display.update()

    def draw_board_navigation(self, chessboard, piece, new_col, new_row, old_col, old_row, old_piece):
        """
        Draws the moves when navigating the previous moves.

        Args:
            board (list): Chessboard as a 2D list.
            piece (object): Piece being moved.
            new_col (int): Starting position column.
            new_row (int): starting position row.
            old_col (int): Original position column.
            old_row (int): Original position row.
            old_piece (object): Piece of there was a capture on the move.
        """
        # Gets the size of the board in x and y.
        num_cols = len(chessboard.board[0])
        num_rows = len(chessboard.board)
        
        # Getting the height and width of the squares
        square_width = WIDTH // num_cols
        square_height = HEIGHT // num_rows

        # Color the piece original square with the correct color.
        fill_color = WHITE if (old_col + old_row) % 2 == 0 else GREEN
        self.win.fill(fill_color, (old_col * square_width, old_row * square_height,
                                        square_width, square_height))
        
        # Color the new square with the correct color. 
        # This clears the square of any pieces that are on that square.
        fill_color = WHITE if (new_col + new_row) % 2 == 0 else GREEN
        self.win.fill(fill_color, (new_col * square_width, new_row * square_height,
                                        square_width, square_height))
        
        # Loads and displays the image of the piece at it's new location.
        img = pygame.image.load(piece.img)
        img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
        img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
        x_pos = new_col * WIDTH // num_cols + img_offset_x
        y_pos = new_row * HEIGHT // num_rows + img_offset_y
        self.win.blit(img, (x_pos, y_pos))

        # Loads and displays the image of the old piece if it was captured.
        if old_piece != []:
            img = pygame.image.load(old_piece.img)
            img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
            img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
            x_pos = old_col * WIDTH // num_cols + img_offset_x
            y_pos = old_row * HEIGHT // num_rows + img_offset_y
            self.win.blit(img, (x_pos, y_pos))

        pygame.display.update()