import pygame


class Over:
    def __init__(self):
        self.image = pygame.image.load("./asset/image/game-over.png").convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self, canvas):
        canvas.blit(self.image, self.rect)
