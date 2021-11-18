import pygame

BRICK_IMG = pygame.transform.scale(pygame.image.load("./asset/image/brick.png").convert_alpha(), (70, 70))


class Brick(pygame.sprite.Sprite):
    def __init__(self, app, position):
        super(Brick, self).__init__()
        self.app = app
        self.image = BRICK_IMG
        self.rect = self.image.get_rect(center=position)
