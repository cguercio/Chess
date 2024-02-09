from graphics import *
from constants import *
from board import *
from pieces import *
from player import *
from utils import *
from game import *
import math
import pygame

def main():
    clock = pygame.time.Clock()
    
    # Initiating the board and drawing squares
    screen = Screen(WIDTH, HEIGHT)
    board = Board(8, 8)
    square_list = board.squares()
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

    # Inititating white piece objects: qs = queens-side, ks = kings-side
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
    player_one = Player(True, WHITE)
    player_two = Player(False, BLACK)
    
    game = Game()

    # Placing the pieces on the board
    for item in Piece.instances:
        board.place_piece(item)

    screen.draw_pieces(board.board)
    
    Piece.game_state = [(thing.x, thing.y, thing.color, thing.is_captured) for thing in Piece.instances]
    
    running = True
    while running:
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
            
            
        while player_one.turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player_one.turn = False
                    player_two.turn = False
                    running = False
                    break
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    state, piece, original_position = player_one.move(mouse_pos, board.board)
                    if state == True and piece.color == WHITE:
                        wait()
                        mouse_pos2 = pygame.mouse.get_pos()
                        new_position = mouse_pos_to_board_pos(mouse_pos2, board.board)
                        temp_board = board.board
                        result, next_board = valid_move(piece, temp_board, new_position, original_position, game, player_one)
                        if result == True:
                            board.board = next_board
                            screen.update_move(board.board, piece, original_position, WHITE, GREEN)
                            player_one.turn = False
                            player_two.turn = True
                            break

                            
        while player_two.turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player_one.turn = False
                    player_two.turn = False
                    running = False
                    break
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    state, piece, original_position = player_two.move(mouse_pos, board.board)
                    if state == True and piece.color == BLACK:
                        wait()
                        mouse_pos2 = pygame.mouse.get_pos()
                        new_position = mouse_pos_to_board_pos(mouse_pos2, board.board)
                        temp_board = board.board
                        result, next_board = valid_move(piece, temp_board, new_position, original_position, game, player_one)
                        if result == True:
                                board.board = next_board
                                screen.update_move(board.board, piece, original_position, WHITE, GREEN)
                                player_two.turn = False
                                player_one.turn = True
                                break



if __name__ == '__main__':
    main()