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
            
def mouse_pos_to_board_pos(pos, chessboard):
    """
    Converts the mouse position to the board position.

    Args:
        pos (tuple): Mouse position.
        board (list): Chessboard as a 2D list.

    Returns:
        tuple: Returns the new board position.
    """
    
    num_cols = len(chessboard.board[0]) # Gets the number of cols by getting the length of the first list
    num_rows = len(chessboard.board) # Gets the number of rows by getting the number of lists
    square_width = WIDTH // num_cols
    square_height = HEIGHT // num_rows

    return (int(math.floor(pos[0] // square_width)), int(math.floor(pos[1] // square_height)))

def valid_move(piece, chessboard, new_position, original_position, game, screen):
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
        print("1")
        return False, chessboard
    if game.piece_in_path(chessboard, new_position, original_position):
        print("2")
        return False, chessboard
    if isinstance(piece, King) and piece.castling == True:
        new_king_position = (6, old_row) if new_col - old_col > 0 else (2, old_row)
        can_castle, chessboard = game.castling(screen, piece, chessboard, new_king_position, original_position)
        piece.castling = False
        print("3")
        return can_castle, chessboard
    if game.can_capture(chessboard, new_position, original_position) == False:
        print("4")
        return False, chessboard
    
    # Updates the temp board with the new move.
    # so we can check for checks on the king.
    captured_piece = chessboard.update_board(piece, new_position, original_position)

    # Check if the piece's king is in check, disallowing movement and resetting the board.
    if game.results_in_check(piece, chessboard) == True:
        chessboard.reset_board(piece, new_position, original_position, captured_piece)
        return False, chessboard
    

    piece.move(new_position)
    return True, chessboard
