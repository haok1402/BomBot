import pygame

from explosion import Explosion
from bomb import Bomb

ENEMY_IMG = {1: pygame.transform.scale(pygame.image.load("./asset/image/robot-2.png").convert_alpha(), (70, 70)),
             2: pygame.transform.scale(pygame.image.load("./asset/image/robot-3.png").convert_alpha(), (70, 70)),
             3: pygame.transform.scale(pygame.image.load("./asset/image/robot-4.png").convert_alpha(), (70, 70))}


class Enemy:
    def __init__(self, app, position, index):
        self.app = app
        self.image = ENEMY_IMG[index]
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.numBomb = 1
        self.numExplosion = 2
        self.velocity = 2
        self.bomb()

    def bomb(self):
        if self.numBomb:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            if self.app.objectBoard[r][c]: return
            self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c))
            self.numBomb -= 1
