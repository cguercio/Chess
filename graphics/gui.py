import pygame
from constants import *
from pieces import *
import os
pygame.init()
pygame.font.init()

class Screen:

    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))

    def draw_squares(self, point_list, color1, color2):
        """
        Iterates over a list of points and fills a checkered pattern

        Args:
            point_list (list): List of points corresponding to the location of squares.
            color1 (RGB): First color to draw.
            color2 (RGB): Second color to draw.
        """

        # Getting the number of rows.
        num_rows = len(point_list)
        point1 = point_list[0][0]
        point2 = point_list[0][1]
        
        square_size = abs(point1[0] - point2[0])
        
        # Iterates over the list of points and fills in the checkered pattern.
        for row in range(num_rows):
            for col, point in enumerate(point_list[row]):
                
                rect_x = point[0]
                rect_y = point[1]
                row_plus_col_is_even = (row + col) % 2 == 0
                
                fill_color = color1 if row_plus_col_is_even else color2
                self.win.fill(fill_color, (rect_x, rect_y,
                                            square_size, square_size))

    def display_image(self, board, piece, location):
        """
        Centers and displays the image of the piece on the square.

        Args:
            board (object): Board object.
            piece (object): Piece being displayed.
            location (tuple): Location to display the piece.
        """
        
        col, row = location
        
        img = pygame.image.load(piece.img)
        
        # Calculating the location the pieces should be displayed to be centered on the square.
        img_offset_x = (WIDTH // board.cols - img.get_width()) // 2 + 2
        img_offset_y = (HEIGHT // board.rows - img.get_height()) // 2 + 2
        x_pos = col * WIDTH // board.cols + img_offset_x
        y_pos = row * HEIGHT // board.rows + img_offset_y
        
        # Blit the image onto the screen.
        self.win.blit(img, (x_pos, y_pos))
        
    def draw_pieces(self, board, omit=None):
        """
        Loops through the board and displays the pieces on the board.

        Args:
            board (object): Board object.
            omit (object, optional): Piece to omit from drawing. Defaults to None.
        """
        for row in board.board:
            for piece in row:
                is_not_omitted_piece = omit != piece
                
                if isinstance(piece, Piece) and is_not_omitted_piece:
                    self.display_image(board, piece, (piece.col, piece.row))
                    
    def clear_squares(self, board, locations):
        """
        Fills squares with the appropriate color to clear the pieces.

        Args:
            board (object): Board Object.
            locations (list): List of tuples(board locations); (col, row)
        """
        
        # Iterates over the locations list.
        for square in locations:
            
            # Unpacking the location tuples.
            col, row = square
            
            # Defining helper variables.
            row_plus_col_is_even = (row + col) % 2 == 0
            rect_x = col * board.square_width
            rect_y = row * board.square_height
        
            # Color the piece original square with the correct color.
            fill_color = WHITE if row_plus_col_is_even else GREEN
            self.win.fill(fill_color, (rect_x, rect_y,
                                            board.square_width, board.square_height))
        

    def update_move(self, board, piece, old_piece, new_position, original_position, navigation=False):
        """
        Calls logic to update the screen with moves when using board navigation.

        Args:
            board (object): Board object.
            piece (object): Piece being moved.
            old_piece (object): Piece being captured.
            new_position (tuple): New position of the piece.
            original_position (tuple): Original position of the piece.
            navigation (bool, optional): Used when navigating previous moves;
                replaces the piece that was captured when undoing moves. Defaults to False.
        """
        
        # Clear the starting and finishing squares of the move.
        self.clear_squares(board, [original_position, new_position])

        # Displays the image of the piece at the new position.
        self.display_image(board, piece, new_position)
        
        # Defining helper variable.
        old_piece_is_not_empty = old_piece != []
        
        # Checks if the old piece was not empty and navigation is True.
        if old_piece_is_not_empty and navigation == True:
            self.display_image(board, old_piece, original_position)

        # Update the screen.
        pygame.display.update()
        
    def display_start_board(self, board, game):
        
        # Iterates backwards through the move list.
        for move in game.move_list[::-1]:
            
            # Unpacking the move dictionary.
            piece = move['current_piece']
            old_square = move['new_square']# Since this function displays previous moves, the old and new squares
            new_square = move["old_square"]# are flipped when unpacking the dictionary.
            old_piece = move["old_piece"]

            # Updating the screen with the move.
            self.update_move(board, piece, old_piece, new_square, old_square, True)
                
                
    def display_previous_move(self, board, game, index):
        """
        Displays the previous move on the screen.

        Args:
            board (object): Board object.
            game (object): Game object.
            index (int): Index used for slicing the move list.
        """
        
        # Iterates over the list of move dictionaries to find the move to undo.
        for move in game.move_list[::-1]:
            
            # Move_to_display describes the current move number minus the number of times
            # the user pressed the right key (index).
            move_to_display = game.move_counter - index
            
            # Is_desired_move checks if the current move number extracted from move dictionary
            # matches the move the user wants to display.
            is_desired_move_number = move['move_number'] == move_to_display
            
            
            if is_desired_move_number:
                
                # Unpacking the move dictionary.
                piece = move['current_piece']
                old_square = move['new_square']# Since this function displays the previous move, the old and new squares
                new_square = move['old_square']# are flipped when unpacking the dictionary.
                old_piece = move["old_piece"]
                
                # Drawing the updated move on the screen.
                self.update_move(board, piece, old_piece, new_square, old_square, True)
            

        
    def display_next_move(self, board, game, index):
        """
        Displays the next move on the board.

        Args:
            board (list): board as a 2D list.
            move_list (list): List of tuples containing information about each move.
            index (int): Index used for slicing the move list.
        """
        
        # Iterates over the move list to find the move to redo.
        for move in game.move_list:
            
            # Move_to_display describes the current move number minus the number of times
            # the user pressed the right key (index).
            move_to_display = game.move_counter - index
            
            # Is_desired_move checks if the current move number extracted from move_list
            # matches the move the user wants to display.
            is_desired_move_number = move['move_number'] == move_to_display
            
            if is_desired_move_number:

                # Extracting the info needed from move list tuple.
                piece = move['current_piece']
                new_square = move['new_square']
                old_square = move['old_square']
                old_piece = []
                    
                # Drawing the updated move on the screen.
                self.update_move(board, piece, old_piece, new_square, old_square, True)
                
    def draw_on_mouse(self, board, piece, square_list):
        """
        Displays the piece on the center of the mouse.

        Args:
            board (object): Board object.
            piece (object): Piece being moved.
            square_list (list): List of tuples of the locations of the squares: (x, y)
        """
        
        # Getting the mouse location on the screen.
        location = pygame.mouse.get_pos()
        col, row = location
        
        # Load piece's image and center it on the mouse.
        img = pygame.image.load(piece.img)
        img_offset_x = img.get_width() // 2
        img_offset_y = img.get_height() // 2
        x_pos = col - img_offset_x
        y_pos = row - img_offset_y
        
        # Redraw the board each tick to clear the image following the mouse.
        self.draw_squares(square_list, WHITE, GREEN)
        
        # Redraw the pieces each tick; omit the piece being moved so it does
        # not show up while moving the piece.
        self.draw_pieces(board, piece)
        
        # Create the piece's transparent surface.
        piece_surface = pygame.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA)
        
        # Blit the image of the piece on the surface.
        piece_surface.blit(img, (0, 0))
        
        # Blit the piece surface on the screen.
        self.win.blit(piece_surface, (x_pos, y_pos))
        
        # Update the pygame window.
        pygame.display.flip()
        
    def display_promotion(self, piece, board):
        """
        Displays the promotion piece images.

        Args:
            piece (object): Piece being moved.
            board (object): Board object.
        """
        
        # Getting a list of null pieces to display their images.
        promotion_pieces = piece.get_promotion_pieces(piece)
        
        # Clear the piece starting square.
        self.clear_squares(board, [(piece.col, piece.row)])

        # Sets the step list so images are displayed at the correct locations
        # depending on if its white or black promoting.
        if piece.color == WHITE:
            step = [0, 1, 2, 3]
        else:
            step = [0, -1, -2, -3]
            
        # Iterates over the step list and displays the images in order
        # one square apart.
        for i, num in enumerate(step):
            
            # Getting location for piece images to be displayed.
            col = piece.col
            row = piece.row + num
            
            promotion_piece = promotion_pieces[i]
            self.display_image(board, promotion_piece, (col, row))
        
        # Updates the display.
        pygame.display.flip()
