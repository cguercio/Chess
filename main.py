from graphics import *
from constants import *
from board import *
from pieces import *

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
    b_rook.move()
    screen.draw_pieces(board.board)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

if __name__ == '__main__':
    main()