import pygame

BRICK_IMG = pygame.transform.scale(pygame.image.load("asset/image/brick.png").convert_alpha(), (70, 70))


class Brick:
    def __init__(self, app, position):
        self.app = app
        self.image = BRICK_IMG
        self.rect = self.image.get_rect(center=position)
