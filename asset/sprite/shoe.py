import pygame

SHOE_IMG = pygame.transform.scale(pygame.image.load("./asset/image/shoe.png").convert_alpha(), (70, 70))


class Shoe:
    def __init__(self, app, position):
        self.app = app
        self.image = SHOE_IMG
        self.rect = self.image.get_rect(center=position)
