from graphics import *
from constants import *
from board import *
from pieces import *
from player import *
from utils import *
import math

def main():
    clock = pygame.time.Clock()
    running = True

    screen = Screen(WIDTH, HEIGHT)
    board = Board(8, 8)
    point_list = board.squares()
    screen.draw_squares(point_list, WHITE, GREEN)
    b_rook = Rook(0, 0, BLACK)
    b_knight = Knight(1, 0, BLACK)
    board.place_piece(b_rook)
    board.place_piece(b_knight)
    player_one = Player()
    screen.draw_squares(point_list, WHITE, GREEN)
    screen.draw_pieces(board.board)
    

    while running:
        clock.tick(FPS)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                move, piece, old_piece_x, old_piece_y = player_one.move(mouse_pos, board.board)
                if move == True:
                    wait()
                    mouse_pos2 = pygame.mouse.get_pos()
                    piece.move(mouse_pos2)
                    board.update_piece(piece, old_piece_x, old_piece_y)
                    screen.draw_squares(point_list, WHITE, GREEN)
                    screen.draw_pieces(board.board)


                    

                
        


if __name__ == '__main__':
    main()