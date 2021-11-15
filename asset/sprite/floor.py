import pygame

FLOOR_IMG = pygame.image.load("./asset/image/floor.png").convert_alpha()


class Floor:
    def __init__(self, app, position):
        self.app = app
        self.image = FLOOR_IMG
        self.rect = self.image.get_rect(topleft=position)
