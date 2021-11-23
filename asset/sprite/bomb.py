import pygame
import random

from asset.sprite.wall import Wall
from asset.sprite.brick import Brick
from asset.sprite.explosion import Explosion
from asset.sprite.shoe import Shoe
from asset.sprite.potion import Potion
from asset.sprite.lightening import Lightening

BOMB_IMG = pygame.transform.scale(pygame.image.load("./asset/image/bomb.png").convert_alpha(), (70, 70))


class Bomb:
    def __init__(self, app, position, bomber):
        self.app = app
        self.image = BOMB_IMG
        self.rect = self.image.get_rect(center=position)
        self.time = 500
        self.bomber = bomber

    def explode(self):
        explosionZone = set()
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        # explosion leftward
        for dc in range(-1, -self.bomber.numExplosion - 1, -1):
            if not (0 <= c + dc < self.app.numCol): break
            nextObject = self.app.objectBoard[r][c + dc]
            if isinstance(nextObject, Wall): break
            explosionZone.add((r, c + dc))
            if isinstance(nextObject, Brick): break
        # explosion upward
        for dr in range(-1, -self.bomber.numExplosion - 1, -1):
            if not (0 <= r + dr < self.app.numCol): break
            nextObject = self.app.objectBoard[r + dr][c]
            if isinstance(nextObject, Wall): break
            explosionZone.add((r + dr, c))
            if isinstance(nextObject, Brick): break
        # explosion rightward
        for dc in range(1, +self.bomber.numExplosion + 1, 1):
            if not (0 <= c + dc < self.app.numCol): break
            nextObject = self.app.objectBoard[r][c + dc]
            if isinstance(nextObject, Wall): break
            explosionZone.add((r, c + dc))
            if isinstance(nextObject, Brick): break
        # explosion downward
        for dr in range(1, +self.bomber.numExplosion + 1, 1):
            if not (0 <= r + dr < self.app.numCol): break
            nextObject = self.app.objectBoard[r + dr][c]
            if isinstance(nextObject, Wall): break
            explosionZone.add((r + dr, c))
            if isinstance(nextObject, Brick): break
        # explosion center
        explosionZone.add((r, c))
        # reload numBomb
        self.bomber.numBomb += 1
        return explosionZone

    def detonate(self):
        if not self.time:
            explosionZone = self.explode()
            for (r, c) in explosionZone:
                if isinstance(self.app.objectBoard[r][c], Brick):
                    randomNum, randomPowerup = random.random(), None
                    if 0 < randomNum <= 0.15: randomPowerup = Shoe(self.app, self.app.getXY(r, c))
                    if 0.15 < randomNum <= 0.30: randomPowerup = Potion(self.app, self.app.getXY(r, c))
                    if 0.30 < randomNum <= 0.45: randomPowerup = Lightening(self.app, self.app.getXY(r, c))
                    self.app.objectBoard[r][c] = Explosion(self.app, self.app.getXY(r, c), randomPowerup)
                else: self.app.objectBoard[r][c] = Explosion(self.app, self.app.getXY(r, c), None)
        if self.time: self.time -= 1
