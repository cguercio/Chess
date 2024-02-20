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

    def display_image(self, chessboard, piece, location):
        """
        Centers and displays the image of the piece on the screen

        Args:
            chessboard (list): Chessboard as a 2D list.
            piece (object): Piece being displayed.
            location (tuple): Location to display the piece.
        """
        
        num_cols = len(chessboard.board[0])
        num_rows = len(chessboard.board)
        col, row = location
        
        img = pygame.image.load(piece.img)
        img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
        img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
        x_pos = col * WIDTH // num_cols + img_offset_x
        y_pos = row * HEIGHT // num_rows + img_offset_y
        self.win.blit(img, (x_pos, y_pos))
        
    def draw_pieces(self, chessboard):
        """
        Loops through the chessboard, finds the pieces, displays the pieces.

        Args:
            board (list): The chessboard as a 2D list
        """

        # Loops through the board and finds the pieces.
        for row in chessboard.board:
            for piece in row:
                if isinstance(piece, Piece):
                    self.display_image(chessboard, piece, (piece.x, piece.y))

        pygame.display.update()
        

    def update_move(self, chessboard, piece, old_piece, new_position, original_position, navigation=False):
        """
        Fills in the old and new squares with the correct color and calls display piece logic.

        Args:
            chessboard (object): Chessboard object.
            piece (object): Piece being moved.
            old_piece (object): Piece being captured if there is one.
            new_position (tuple): New location of the piece being moved.
            original_position (tuple): Original location of the piece being moved.
            navigation (bool, optional): True if using board navigation option. Defaults to False.
        """
            
        # Gets the size of the board in x and y.
        num_cols = len(chessboard.board[0])
        num_rows = len(chessboard.board)

        # Calculating the height and width of the squares.
        square_width = self.width // num_cols
        square_height = self.height // num_rows

        # Unpacking the location tuples.
        old_col, old_row = original_position
        new_col, new_row = new_position    

        # Color the piece original square with the correct color.
        fill_color = WHITE if (old_col + old_row) % 2 == 0 else GREEN
        self.win.fill(fill_color, (old_col * square_width, old_row * square_height,
                                            square_width, square_height))
        
        # Color the new square with the correct color. 
        # This clears the square of any pieces that are on that square.
        fill_color = WHITE if (new_col + new_row) % 2 == 0 else GREEN
        self.win.fill(fill_color, (new_col * square_width,new_row * square_height,
                                            square_width, square_height))

        self.display_image(chessboard, piece, (new_col, new_row))
        
        # If using board navigation and there was a piece on the board.
        if old_piece != [] and navigation == True:
            self.display_image(chessboard, old_piece, (old_col, old_row))

        
        pygame.display.update()
        
    def display_start_board(self, chessboard, move_list):
        """
        Displays the starting board.

        Args:
            chessboard (list): Chessboard as a 2D list.
            move_list (list): List of tuples containing information about each move.
        """
        
        for move in move_list[::-1]:
            piece = move[1]
            old_col, old_row = move[2]
            new_col, new_row = move[3]
            old_piece = move[4]

            self.update_move(chessboard, piece, old_piece, (new_col, new_row), (old_col, old_row), True)
                
    def display_previous_move(self, chessboard, game, index):
        """
        Displays the previous move on the board.

        Args:
            chessboard (list): Chessboard as a 2D list.
            move_list (list): List of tuples containing information about each move.
            index (int): Index used for slicing the move list.
        """
        
        # Iterates over the move list to find the move to undo.
        for move in game.move_list[::-1]:
            if move[0] == game.move_counter - index:
                
                # Extracting the info needed from move list tuple.
                piece = move[1]
                old_col, old_row = move[2]
                new_col, new_row = move[3]
                old_piece = move[4]
                
                # Drawing the updated move on the screen.
                self.update_move(chessboard, piece, old_piece, (new_col, new_row), (old_col, old_row), True)

        
    def display_next_move(self, chessboard, game, index):
        """
        Displays the next move on the board.

        Args:
            chessboard (list): Chessboard as a 2D list.
            move_list (list): List of tuples containing information about each move.
            index (int): Index used for slicing the move list.
        """
        
        # Iterates over the move list to find the move to redo.
        for move in game.move_list:
            if move[0] == game.move_counter - index:

                # Extracting the info needed from move list tuple.
                piece = move[1]
                new_col, new_row = move[2]
                old_col, old_row = move[3]
                old_piece = []
                    
                # Drawing the updated move on the screen.
                self.update_move(chessboard, piece, old_piece, (new_col, new_row), (old_col, old_row), True)
