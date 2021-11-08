import pygame


class Bomb:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/bomb.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.time = 1000
