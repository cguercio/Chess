import pygame
import math
from constants import *
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
        for row in range(8):
            point = (point_list[row][0])
            self.win.fill(WHITE, (point[0], point[1], 100, 100))

            for col in range(1,8, 1):
                point = (point_list[row][col])
                self.win.fill(BLACK, (point[0], point[1], 100, 100))


        pygame.display.update()
