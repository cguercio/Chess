from graphics import *
from constants import *
from board import *

def main():
    clock = pygame.time.Clock()
    running = True

    screen = Screen(WIDTH, HEIGHT)
    board = Board(8, 8, WHITE, BLACK)
    point_list = board.squares()
    screen.draw_squares(point_list)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

if __name__ == '__main__':
    main()