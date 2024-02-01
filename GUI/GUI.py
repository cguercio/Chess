import pygame
pygame.init()
pygame.font.init()


BLACK = (0, 0, 0)

class Screen:

    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode(self.width, self.height)

    def display(self):
        self.win.fill(BLACK)
        pygame.display.update()