import pygame

WALL_IMG = pygame.transform.scale(pygame.image.load("./asset/image/wall.png").convert_alpha(), (70, 70))


class Wall:
    def __init__(self, app, position):
        self.app = app
        self.image = WALL_IMG
        self.rect = self.image.get_rect(center=position)
