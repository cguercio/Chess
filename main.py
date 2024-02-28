from graphics import *
from constants import *
from board import *
from pieces import *
from player import *
from game import *
import pygame

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
    
    # Initiating the board and drawing squares
    screen = Screen(WIDTH, HEIGHT)
    chessboard = Board(8, 8, WIDTH, HEIGHT)
    square_list = chessboard.squares()
    screen.draw_squares(square_list, WHITE, GREEN)

    # Initiating black piece objects: qs = queens-side, ks = kings-side
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

    # Initiating white piece objects: qs = queens-side, ks = kings-side
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

    # Initiating player objects
    player = Player()

    # Initiating the game object.
    game = Game()

    # Placing the pieces on the board.
    for item in Piece.instances:
        chessboard.place_piece(item)

    # Draws the pieces at their starting squares.
    screen.draw_pieces(chessboard)
    pygame.display.update()
    
    index = 0

    running = True
    while running:

        clock.tick(FPS)

        # Quit pygame if escape is clicked.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

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

            move = False
            mouse_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.draw_squares(square_list, WHITE, GREEN)
                screen.draw_pieces(chessboard)
                pygame.display.update()
                index = 0
            
                mouse_pos = pygame.mouse.get_pos()
                board_position = chessboard.get_board_position(mouse_pos)
                piece = chessboard.get_square_contents(board_position)
                
                piece_selected = True if piece != [] else False
                
                if (piece_selected == True and piece.color == WHITE and game.move_counter % 2 == 0
                    or piece_selected == True and piece.color == BLACK and game.move_counter % 2 != 0):
                    mouse_down = True
                    
                while mouse_down:
                    clock.tick(FPS)
                    
                    screen.draw_on_mouse(chessboard, piece, square_list)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 3:
                                move = False
                                mouse_down = False
                                screen.draw_squares(square_list, WHITE, GREEN)
                                screen.draw_pieces(chessboard)
                                pygame.display.flip()
                                break
                        
                        if event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos() != mouse_pos:
                            move = True
                            mouse_down = False
                            mouse_pos2 = pygame.mouse.get_pos()
                            break
                        elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos() == mouse_pos:
                            mouse_down = False
                            screen.draw_squares(square_list, WHITE, GREEN)
                            screen.draw_pieces(chessboard)
                            pygame.display.flip()
                            
                            if mouse_click():
                                mouse_pos2 = pygame.mouse.get_pos()
                                move = True
                                mouse_down = False
                                break
                            else:
                                move = False
                                mouse_down = False
                                screen.draw_squares(square_list, WHITE, GREEN)
                                screen.draw_pieces(chessboard)
                                pygame.display.flip()
                                break


                
            # Checks if the user tried to move a piece.
            if move == True:
                original_position = (piece.col, piece.row)
                new_position = chessboard.get_board_position(mouse_pos2)
                old_piece = chessboard.board[new_position[0]][new_position[1]]
                
                if old_piece != [] and old_piece.color == piece.color:
                    old_piece = []
                    
                
                if (piece.is_valid_move(new_position, original_position) == False
                    or game.piece_in_path(chessboard.board, new_position, new_position) == True):
                    valid_move = False
                    
                elif isinstance(piece, King) and piece.castling == True:
                    
                    new_king_position = piece.castle_right if new_position[0] - original_position[0] > 0 else piece.castle_left
                        
                    if game.can_castle(screen, piece, chessboard, new_king_position, original_position) == False:
                        valid_move = False
                    else:
                        valid_move = True
                        
                elif game.can_capture(piece, chessboard.board, new_position, original_position) == False:
                    valid_move = False
                    
                else:

                    captured_piece = chessboard.update_board(piece, new_position, original_position)

                    # Check if the piece's king is in check, disallowing movement and resetting the board.
                    if game.results_in_check(piece, chessboard.board) == True:
                        print("false")
                        chessboard.reset_board(piece, new_position, original_position, captured_piece)
                        valid_move = False
                    else:
                        piece.move(new_position)
                        valid_move = True
                    
                
                # Checks if a pawn reaches the edge of the board and it was a valid move.
                if valid_move == True and isinstance(piece, Pawn) and piece.row in [0,7]:
                    
                    # Updates the move list with the pawn move.
                    
                    screen.display_promotion(piece, chessboard)
                    
                    if not mouse_click():
                        valid_move == False
                        move = False
                        piece.move(original_position)
                        chessboard.reset_board(piece, new_position, original_position, old_piece)
                        screen.draw_squares(square_list, WHITE, GREEN)
                        screen.draw_pieces(chessboard)
                        pygame.display.flip()
                        
                    else:
                        game.move_list.append((game.move_counter, piece, new_position, original_position, old_piece))
                        clicked_position = chessboard.get_board_position(pygame.mouse.get_pos())
                        promoted_pawn = piece.select_promotion(clicked_position)
                        
                        # Updates the move list with the queen move. This way the move list has all information.
                        game.move_list.append((game.move_counter, promoted_pawn, new_position, original_position, old_piece))
                        
                        screen.draw_squares(square_list, WHITE, GREEN)
                        screen.draw_pieces(chessboard)
                        pygame.display.flip()
                        
                        move = False
                        valid_move == False
                        game.move_counter += 1
                        
                
                # Checks if the move was valid and updates the board, screen, and move list.
                elif valid_move == True:
                    
                    screen.draw_squares(square_list, WHITE, GREEN)
                    screen.draw_pieces(chessboard)
                    pygame.display.flip()
                    game.move_list.append((game.move_counter, piece, (piece.col, piece.row), original_position, old_piece))
                    
                    move = False
                    valid_move == False
                    game.move_counter += 1
                
                elif valid_move == False:
                    move = False
                    valid_move == False
                    screen.draw_squares(square_list, WHITE, GREEN)
                    screen.draw_pieces(chessboard)
                    pygame.display.flip()
                    
                game.in_check(chessboard.board)
                
                if w_king.in_check and game.is_checkmate(chessboard, w_king):
                    print("Game Over! Black Wins!")
                
                elif b_king.in_check and game.is_checkmate(chessboard, b_king):
                    print("Game Over! White Wins!")
                        
        
if __name__ == '__main__':
    main()