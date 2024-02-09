import pygame
import math
from constants import *
from pieces import *
from game import *


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            
# This function converts the mouse position to the position of the board.
def mouse_pos_to_board_pos(pos, board):
    
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
        print("2")
        return False, board
    if game.piece_path(board, new_position, original_position) == False:
        print("3")
        return False, board
    if game.can_capture(board, new_position, original_position) == False:
        print("4")
        return False, board
    
    # Updates the is_captured attribute if there is a piece on the new square.
    if  board[new_col][new_row] != []:
        board[new_col][new_row].is_captured = True

    # Updates the board. We do not update the piece locations yet
    # because we still have to check if the player is in check.
    # Here we update the board and use it as a temporary board.
    # The real board is updated using the piece object locations.
    board[old_col][old_row] = []
    board[new_col][new_row] = piece
    
    # Finds the location of the kings on the new board.
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
    if w_king.is_captured == True and player.color == WHITE:
        return False, board
    elif b_king.is_captured == True and player.color == BLACK:
        return False, board
    
    # Moves the piece to its new location.
    piece.move(new_position)
    
    # Generates a list of attributes for each piece so the game
    # state can be stored. This is used to reset the board if a move is
    # invalid and its used to go through previous positions.
    temp_list = []
    for thing in Piece.instances:
        state = (thing.x, thing.y, thing.color, thing.is_captured)
        temp_list.append(state)
    # Appends the list of attributes to the game_state list.
    Piece.game_state.append(temp_list)

    return True, board