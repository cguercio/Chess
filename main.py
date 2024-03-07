from graphics import *
from constants import *
from board import *
from pieces import *
from game import *
import pygame

board_location = (0, 0)

def mouse_click():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return True
                if event.button == 3:
                    return False

def main():
    clock = pygame.time.Clock()
    
    # Instantiating objects.
    screen = Screen(WIDTH, HEIGHT)
    chessboard = Board(8, 8, WIDTH, HEIGHT, board_location)
    game = Game()
    
    # Instantiating white piece objects: qs = queens-side, ks = kings-side
    qs_rook = Rook(0, 7, WHITE)
    qs_knight = Knight(1, 7, WHITE)
    qs_bishop = Bishop(2, 7, WHITE)
    w_queen = Queen(3, 7, WHITE)
    w_king = King(4, 7, WHITE)
    ks_bishop = Bishop(5, 7, WHITE)
    ks_knight = Knight(6, 7, WHITE)
    ks_rook = Rook(7, 7, WHITE)
    wpawn1 = Pawn(0, 6, WHITE)
    wpawn2 = Pawn(1, 6, WHITE)
    wpawn3 = Pawn(2, 6, WHITE)
    wpawn4 = Pawn(3, 6, WHITE)
    wpawn5 = Pawn(4, 6, WHITE)
    wpawn6 = Pawn(5, 6, WHITE)
    wpawn7 = Pawn(6, 6, WHITE)
    wpawn8 = Pawn(7, 6, WHITE)
    
    # Instantiating black piece objects: qs = queens-side, ks = kings-side
    qs_rook = Rook(0, 0, BLACK)
    qs_knight = Knight(1, 0, BLACK)
    qs_bishop = Bishop(2, 0, BLACK)
    b_queen = Queen(3, 0, BLACK)
    b_king = King(4, 0, BLACK)
    ks_bishop = Bishop(5, 0, BLACK)
    ks_knight = Knight(6, 0, BLACK)
    ks_rook = Rook(7, 0, BLACK)
    bpawn1 = Pawn(0, 1, BLACK)
    bpawn2 = Pawn(1, 1, BLACK)
    bpawn3 = Pawn(2, 1, BLACK)
    bpawn4 = Pawn(3, 1, BLACK)
    bpawn5 = Pawn(4, 1, BLACK)
    bpawn6 = Pawn(5, 1, BLACK)
    bpawn7 = Pawn(6, 1, BLACK)
    bpawn8 = Pawn(7, 1, BLACK)

    # Updating the initial board with the pieces.
    for item in Piece.instances:
        chessboard.place_piece(item)

    # Draws squares and pieces on the screen.
    square_list = chessboard.squares()
    screen.draw_squares(square_list, WHITE, GREEN)
    screen.draw_pieces(chessboard)
    pygame.display.update()
    

    index = 0
    running = True
    while running:

        # Locks while loop tick.
        clock.tick(FPS)

        # Detects pygame events.
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                break

            ### This section is for navigating the board using the arrow keys.
            ### This does not change the board. This only updates the screen visually.
            
            # Displays the beginning of the move list.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and game.move_counter - index > 0:
                    screen.display_start_board(chessboard, game)
                    index = game.move_counter

                # Displays the previous move if the user presses left.
                if event.key == pygame.K_LEFT:
                    index += 1 # It is important that this index is before the function
                    if game.move_counter - index >= 0:
                        screen.display_previous_move(chessboard, game, index)
                    else:
                        index = game.move_counter
                    
                # Displays the next move if the user presses right.
                if event.key == pygame.K_RIGHT and index > 0:
                    screen.display_next_move(chessboard, game, index)
                    index -= 1

                # Displays the current board and escapes from board navigation.
                if event.key in [pygame.K_ESCAPE, pygame.K_UP]:
                    screen.draw_squares(square_list, WHITE, GREEN)
                    screen.draw_pieces(chessboard)
                    pygame.display.update()
                    index = 0
            
            ### This section contains the logic for detecting if the user has made a move.
            move = False # Move is only true if the user selected a piece of their color and tried to move it to a new square.
            mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Draws the current board on the screen in case the user was looking at previous moves.
                index = 0
                screen.draw_squares(square_list, WHITE, GREEN)
                screen.draw_pieces(chessboard)
                pygame.display.update()
                
                # Getting the mouse position when the user clicks the mouse button.
                mouse_pos = pygame.mouse.get_pos()
                
                # Converting the mouse position to the board position.
                board_position = chessboard.get_board_position(mouse_pos)
                board_col, board_row = board_position
                
                # Checking if the board position is valid.
                if board_col is None or board_row is None:
                    piece_selected = False

                else:
                    # Get the contents of the board position.
                    piece = chessboard.get_square_contents(board_position)
                    piece_selected = True if piece != [] else False
                
                
                # Defining helper variable.
                piece_is_selected = piece_selected == True
                
                if piece_is_selected:
                    
                    # Defining helper variables.
                    piece_is_white = piece.color == WHITE
                    is_whites_turn = game.move_counter % 2 == 0 # White's turn if move number is even.
                    piece_is_black = piece.color == BLACK
                    is_blacks_turn = game.move_counter % 2 != 0 # Black's turn if move number is odd.
                    
                    # Checks if the user is trying to move a piece that is the correct color's turn.
                    if (piece_is_white and is_whites_turn
                        or piece_is_black and is_blacks_turn):
                        mouse_down = True
                    
                # Loops while the user is holding the mouse down.
                while mouse_down:
                    
                    # Locks while loop tick.
                    clock.tick(FPS)
                    
                    # Draws the piece the user picked up on the mouse position.
                    screen.draw_on_mouse(chessboard, piece, square_list)
                    
                    # Getting pygame events.
                    for event in pygame.event.get():
                        
                        # Checks if the user pressed the right mouse button.
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # If user presses the right mouse button, reset the board, break the loop.
                            if event.button == 3:
                                mouse_down = False
                                screen.draw_squares(square_list, WHITE, GREEN)
                                screen.draw_pieces(chessboard)
                                pygame.display.flip()
                                break
                        
                        # Defining helper variables.
                        mouse_button_released = event.type == pygame.MOUSEBUTTONUP
                        mouse_didnt_move = pygame.mouse.get_pos() == mouse_pos
                        mouse_moved = pygame.mouse.get_pos() != mouse_pos
                        
                        # If the user released the mouse button and moved the mouse, try to make a move.
                        if mouse_button_released and mouse_moved:
                            move = True
                            mouse_down = False
                            new_mouse_position = pygame.mouse.get_pos()
                            break
                        
                        # If the user released the mouse button and didnt move the mouse, reset the board
                        # and wait for user to click a square to move to.
                        elif mouse_button_released and mouse_didnt_move:
                            mouse_down = False
                            screen.draw_squares(square_list, WHITE, GREEN)
                            screen.draw_pieces(chessboard)
                            pygame.display.flip()
                            
                            # If user clicked a new square, try to make the move.
                            if mouse_click():
                                new_mouse_position = pygame.mouse.get_pos()
                                move = True
                                mouse_down = False
                                break
                            
                            # If used didn't click a new square, reset the board and wait for a new move.
                            else:
                                mouse_down = False
                                screen.draw_squares(square_list, WHITE, GREEN)
                                screen.draw_pieces(chessboard)
                                pygame.display.flip()
                                break


            ### This section contains the logic to determine of the move the user tried to play is valid.
            # Checks if the user tried to move a piece.
            valid_move = False
            if move == True:
                
                # Get the square the piece was on.
                old_square = (piece.col, piece.row)
                
                # Gets the square the user tried to move to.
                new_square = chessboard.get_board_position(new_mouse_position)
                new_col, new_row = new_square
                
                if new_col is not None and new_row is not None:
                    
                    # Getting the contents of the new square.
                    old_piece = chessboard.get_square_contents(new_square)
                
                    # Sets the contents of the old pieces to empty list if the old pieces is the same color as the piece being moved.
                    # Usually this is not needed because trying to capture a piece of the same color would result in an invalid move.
                    # This check is for castling; so the user can castle by placing their king on their rook.
                    if old_piece != [] and old_piece.color == piece.color:
                        old_piece = []
                
                    # Defining helper variables.
                    not_valid_piece_move = piece.is_valid_move(new_square, old_square) == False
                    piece_in_path = game.piece_in_path(chessboard.board, old_square, new_square) == True
                    
                    # Checks if the move is valid for that type of piece and if there are pieces in the way of the move.
                    if not_valid_piece_move or piece_in_path:
                        valid_move = False
                        
                    # Checks if the piece is a king and is trying to castle.
                    elif isinstance(piece, King) and piece.castling == True:
                        
                        # Sets the new king position depending on the side of the castling move.
                        new_king_position = piece.castle_right if new_square[0] - old_square[0] > 0 else piece.castle_left
                            
                        # Defining helper variables.
                        can_castle = game.can_castle(screen, piece, chessboard, old_square, new_king_position) == True
                        
                        # Checks the conditions for castling.
                        if can_castle:
                            valid_move = True
                    
                    # Check if the piece can capture at the new square.
                    elif game.can_capture(piece, chessboard.board, old_square, new_square) == False:
                        valid_move = False
                    
                    # If move passes all move checks, check if the move results in check.
                    else:
                        
                        # Update the board and and get the piece that was captured.
                        captured_piece = chessboard.update_board(piece, old_square, new_square)

                        # Check if the piece's king is in check, disallowing movement and resetting the board.
                        if game.results_in_check(piece, chessboard.board):
                            
                            chessboard.reset_board(piece, old_square, new_square, captured_piece)
                            
                            # If piece is a pawn, reset the enpassant attribute.
                            if isinstance(piece, Pawn):
                                piece.enpassant = False
                                
                            valid_move = False
                            
                        # If move doesn't result in check, update the piece position and set valid move.
                        else:
                            piece.move(new_square)
                            valid_move = True
                            
                ### This section contains the logic of updating the board and screen with a valid move.
                ### This section also checks for promoting pawns and En Passant moves.
                # Checks if a pawn reaches the edge of the board and it was a valid move.
                if valid_move == True and isinstance(piece, Pawn) and piece.row in [0,7]:
                    
                    # Displays the promotion pieces on the screen for user to select.
                    screen.display_promotion(piece, chessboard)
                    
                    # Checks if the user cancels pawn promotion. Resets the board, moves the pawn back to its original square.
                    if not mouse_click():
                        valid_move == False
                        move = False
                        piece.move(old_square)
                        chessboard.reset_board(piece, old_square, new_square, old_piece)
                        screen.draw_squares(square_list, WHITE, GREEN)
                        screen.draw_pieces(chessboard)
                        pygame.display.flip()
                        
                    else:
                        
                        # Updates the move list with the pawn move.
                        game.update_move_list(game.move_counter, piece, old_square, new_square, old_piece)
                        
                        # Gets the board position the user clicked on when selecting the piece to promote.
                        clicked_position = chessboard.get_board_position(pygame.mouse.get_pos())
                        
                        # Gets the promoted pieces based on where user clicked.
                        promoted_pawn = piece.select_promotion(clicked_position)
                        
                        # Updates the board with the new piece at the new square.
                        chessboard.update_board(promoted_pawn, old_square, new_square)
                        
                        # Updates the move list the promoted piece. This way the move list has all information.
                        game.update_move_list(game.move_counter, promoted_pawn, old_square, new_square, old_piece)
                        
                        # Draws the new move on the screen.
                        screen.draw_squares(square_list, WHITE, GREEN)
                        screen.draw_pieces(chessboard)
                        pygame.display.flip()
                        
                        # Updates the move counter at the end of the move.
                        game.move_counter += 1
                        
                # Checks if a pawn is trying En Passant.
                elif valid_move == True and isinstance(piece, Pawn) and piece.enpassant == True:
                    
                    # Update the board with the new pawn move.
                    chessboard.update_board(piece, old_square, new_square)
                    
                    # Updates the move list with the pawn move.
                    game.update_move_list(game.move_counter, piece, old_square, new_square, old_piece)
                    
                    # If the pawn is white, update the board by removing the pawn behind it as a capture.
                    if piece.color == WHITE:
                        captured_pawn_location = (piece.col, piece.row + 1)
                        captured_piece = chessboard.update_board([], old_square, captured_pawn_location)
                        
                    # If the pawn is black, update the board by removing the pawn behind it as a capture.
                    else:
                        captured_pawn_location = (piece.col, piece.row - 1)
                        captured_piece = chessboard.update_board([], old_square, captured_pawn_location)
                        
                    # Update the move list with the capture.
                    game.update_move_list(game.move_counter, [], (captured_piece.col, captured_piece.row), (captured_piece.col, captured_piece.row), captured_piece)
                        
                    # Draws the new move on the screen.
                    screen.draw_squares(square_list, WHITE, GREEN)
                    screen.draw_pieces(chessboard)
                    pygame.display.flip()
                    
                    # Sets the En Passant attribute to false so that the pawn cannot En Passant again.
                    piece.enpassant = False
                    
                    # Updates the move counter at the end of the move.
                    game.move_counter += 1
                    
                # If move was valid and no special moves are made.
                elif valid_move == True:
                    
                    # Draws the new move on the screen.
                    screen.draw_squares(square_list, WHITE, GREEN)
                    screen.draw_pieces(chessboard)
                    pygame.display.flip()
                    
                    # Updates the move list with the new move.
                    game.update_move_list(game.move_counter, piece, old_square, new_square, old_piece)
                    
                    # Updates the move counter at the end of the move.
                    game.move_counter += 1
                
                # If move was not valid reset the screen.
                elif valid_move == False:
                    screen.draw_squares(square_list, WHITE, GREEN)
                    screen.draw_pieces(chessboard)
                    pygame.display.flip()
                
                ### This section checks the board for checkmate on either side.
                # Set the list of checking pieces to empty.
                game.check_list = []
                
                # Check if either king is in check.
                game.in_check(chessboard.board)
                
                # Check if white king is in check and check for checkmate conditions.
                if w_king.in_check and game.is_checkmate(chessboard, w_king):
                    print("Game Over! Black Wins!")
                
                # Check if white king is in check and check for checkmate conditions.
                elif b_king.in_check and game.is_checkmate(chessboard, b_king):
                    print("Game Over! White Wins!")
                
                # Clear the list of checking pieces.
                game.check_list = []
                
if __name__ == '__main__':
    main()