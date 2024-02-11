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

def valid_move(piece, board, new_position, original_position, game, player, screen):
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
    old_piece = board[new_col][new_row]
    
    # Runs different checks for valid moves.
    if piece.valid_move(new_position, original_position) == False:
        return False, board
    if game.piece_path(board, new_position, original_position) == False:
        return False, board
    if isinstance(piece, King) and piece.castling == True:
        game.castling(screen, piece, board, new_position, original_position)
        piece.move(new_position)
        return True, board
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
        if old_piece != []:
            board[new_col][new_row] = old_piece

        return False, board
    elif b_king.in_check == True and player.color == BLACK:
        board[old_col][old_row] = piece
        board[new_col][new_row] = []
        w_king.in_check = False
        if old_piece != []:
            board[new_col][new_row] = old_piece
        return False, board
    
    # Updates the piece location.
    piece.move(new_position)

    return True, board



def board_navigation(screen, board, move_list, index, key):
    """
    Cycles through the move list forwards or backwards.

    Args:
        screen (object): Screen object.
        board (list): Chessboard as a 2D list.
        move_list (list): List of tuples containing previous move info.
        index (int): Index for iterating over move list.
        key (key): Pygame key press.

    Returns:
        boolean: Returns false if index is at the start or end of the list.
    """
    
    # If use presses the down arrow go to the start of the move list.
    if key == pygame.K_DOWN:
        for move in move_list[::-1]:
            piece = move[0]
            old_col, old_row = move[1]
            new_col, new_row = move[2]
            old_piece = move[3]

            screen.draw_board_navigation(board, piece, new_col, new_row, old_col, old_row, old_piece)

    # If key is left arrow, visually undo the moves.
    if key == pygame.K_LEFT:

        # If we are at the start of the list, return false.
        if len(move_list) - index < 0:
            return False

        else:
            # Finding the move to undo by slicing the move list with index.
            move = move_list[len(move_list) - index]

            # Extracting the info needed from move list tuple.
            piece = move[0]
            old_col, old_row = move[1]
            new_col, new_row = move[2]
            old_piece = move[3]

            # Drawing the updated move on the screen.
            screen.draw_board_navigation(board, piece, new_col, new_row, old_col, old_row, old_piece)
            
    # If key is right arrow, visually redo the moves.
    if key == pygame.K_RIGHT:

        # If we are at the end of the list, return false.
        if index == 0:
            return False
        else:
            # Finding the move to undo by slicing the move list with index.
            move = move_list[len(move_list) - index]

            # Extracting the info needed from move list tuple.
            piece = move[0]
            new_col, new_row = move[1]
            old_col, old_row = move[2]
            old_piece =[]

            # It is important that this index is after the function
            index -= 1

            # Drawing the updated move on the screen.
            screen.draw_board_navigation(board, piece, new_col, new_row, old_col, old_row, old_piece)
            