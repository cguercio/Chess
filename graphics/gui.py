import pygame
pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Screen:

    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))

    def draw_squares(self, point_list):

        for point in point_list:
            self.win.fill(WHITE, (point[0], point[1], point_list[1][0] - point_list[0][0],
                                   point_list[1][1] - point_list[0][1]))

        pygame.display.update()
