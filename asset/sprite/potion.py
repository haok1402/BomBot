import pygame

POTION_IMG = pygame.transform.scale(pygame.image.load("./asset/image/potion.png").convert_alpha(), (70, 70))


class Potion:
    def __init__(self, app, position):
        self.app = app
        self.image = POTION_IMG
        self.rect = self.image.get_rect(center=position)
