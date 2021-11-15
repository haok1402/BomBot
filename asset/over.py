import pygame

OVER_IMG = pygame.image.load("./asset/image/over.png").convert_alpha()


class Over:
    def __init__(self, app, position):
        self.app = app
        self.image = OVER_IMG
        self.image.set_alpha(215)
        self.rect = self.image.get_rect(center=position)
