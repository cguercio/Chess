from graphics import gui
import pygame


def main():
    clock = pygame.time.Clock()
    running = True

    screen = gui.Screen(WIDTH, HEIGHT)
    screen.draw_squares()

    while running:
        clock.tick(FPS)

        for event in gui.pygame.event.get():
            if event.type == gui.pygame.QUIT:
                running = False
                break

if __name__ == '__main__':
    main()