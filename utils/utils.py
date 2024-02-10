import pygame
import math
from constants import *
from pieces import *
from game import *
from graphics import *


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            
def mouse_pos_to_board_pos(pos, board):
    """
    Converts the mouse position to the board position.

    Args:
        pos (tuple): Mouse position.
        board (list): Chessboard as a 2D list.

    Returns:
        tuple: Returns the new board position.
    """
    
    num_cols = len(board[0]) # Gets the number of cols by getting the length of the first list
    num_rows = len(board) # Gets the number of rows by getting the number of lists
    square_width = WIDTH // num_cols
    square_height = HEIGHT // num_rows

    return (int(math.floor(pos[0] // square_width)), int(math.floor(pos[1] // square_height)))

def valid_move(piece, board, new_position, original_position, game, player):
    """
    Checks if the current move is a valid move.

    Args:
        piece (object): Piece to be moved.
        board (list): Chessboard as a 2D list.
        new_position (tuple): Position to which the piece is to be moved.
        original_position (tuple): Original position of piece.
        game (object): Game object to call methods on.
        player (object): Player currently making a move.
    """
    
    # Unpacks the original and new piece positions.
    old_col, old_row = original_position
    new_col, new_row = new_position
    
    # Runs different checks for valid moves.
    if piece.valid_move(new_position, original_position) == False:
        return False, board
    if game.piece_path(board, new_position, original_position) == False:
        return False, board
    if game.can_capture(board, new_position, original_position) == False:
        return False, board

    # Updates the temp board with the new move 
    # so we can check for checks on the king.
    board[old_col][old_row] = []
    board[new_col][new_row] = piece
    
    # Finds the location of the kings on the temp board.
    # We cannot use the king objects to find the locations
    # here because the pieces has not moved yet.
    for col, rank in enumerate(board):
        for row, item in enumerate(rank):
            if isinstance(item, King) and item.color == WHITE:
                white_king = (col, row)
                w_king = item
            elif isinstance(item, King) and item.color == BLACK:
                black_king = (col, row)
                b_king = item
    
    # Checking if the kings are in check and updating their attribute.
    game.in_check(board, white_king, black_king, w_king, b_king)

    # Checks if the player tries to make a move, but their king is still in check.
    if w_king.in_check == True and player.color == WHITE:
        board[old_col][old_row] = piece
        board[new_col][new_row] = []
        b_king.in_check = False
        return False, board
    elif b_king.in_check == True and player.color == BLACK:
        board[old_col][old_row] = piece
        board[new_col][new_row] = []
        w_king.in_check = False
        return False, board
    
    # Updates the piece location.
    piece.move(new_position)

    return True, board



def board_history(screen, board, move_list, point_list, stop,  color1, color2):

            for move in move_list[-1:stop - 1:-1]:
                item = move[0]
                old_col, old_row = move[1]
                new_col, new_row = move[2]
                old_piece = move[3]

                board[old_col][old_row] = old_piece
                board[new_col][new_row] = item
                
            screen.draw_squares(point_list, color1, color2)

            num_cols = len(board[0])
            num_rows = len(board)

            # Loops through the board, finds the pieces, centers and displays the pieces
            for col, rank in enumerate(board):
                for row, piece in enumerate(rank):
                    if isinstance(piece, Piece):
                        img = pygame.image.load(piece.img)
                        img_offset_x = (WIDTH // num_cols - img.get_width()) // 2 + 2
                        img_offset_y = (HEIGHT // num_rows - img.get_height()) // 2 + 2
                        x_pos = col * WIDTH // num_cols + img_offset_x
                        y_pos = row * HEIGHT // num_rows + img_offset_y
                        screen.win.blit(img, (x_pos, y_pos))
            pygame.display.update()


        # for event in pygame.event.get():
        #     if event.key == pygame.K_LEFT:
        #         if event.type == pygame.K_ESCAPE:
        #             board_state = False



