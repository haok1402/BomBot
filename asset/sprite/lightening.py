import pygame

LIGHTENING_IMG = pygame.transform.scale(pygame.image.load("./asset/image/lightening.png").convert_alpha(), (70, 70))


class Lightening:
    def __init__(self, app, position):
        self.app = app
        self.image = LIGHTENING_IMG
        self.rect = self.image.get_rect(center=position)
