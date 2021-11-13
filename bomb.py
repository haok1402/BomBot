import pygame

from wall import Wall
from brick import Brick
from explosion import Explosion

BOMB_IMG = pygame.transform.scale(pygame.image.load("./asset/image/bomb.png").convert_alpha(), (70, 70))


class Bomb:
    def __init__(self, app, position):
        self.app = app
        self.image = BOMB_IMG
        self.rect = self.image.get_rect(center=position)
        self.time = 500

    def detonate(self):
        if not self.time:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            # explosion leftward
            for dc in range(-1, -self.app.robot.numExplosion - 1, -1):
                if not (0 <= c + dc < self.app.numCol): break
                nextObject = self.app.objectBoard[r][c + dc]
                if isinstance(nextObject, Wall): break
                self.app.objectBoard[r][c + dc] = Explosion(self.app, self.app.getXY(r, c + dc))
                if isinstance(nextObject, Brick): break
            # explosion upward
            for dr in range(-1, -self.app.robot.numExplosion - 1, -1):
                if not (0 <= r + dr < self.app.numCol): break
                nextObject = self.app.objectBoard[r + dr][c]
                if isinstance(nextObject, Wall): break
                self.app.objectBoard[r + dr][c] = Explosion(self.app, self.app.getXY(r + dr, c))
                if isinstance(nextObject, Brick): break
            # explosion rightward
            for dc in range(1, +self.app.robot.numExplosion + 1, 1):
                if not (0 <= c + dc < self.app.numCol): break
                nextObject = self.app.objectBoard[r][c + dc]
                if isinstance(nextObject, Wall): break
                self.app.objectBoard[r][c + dc] = Explosion(self.app, self.app.getXY(r, c + dc))
                if isinstance(nextObject, Brick): break
            # explosion downward
            for dr in range(1, +self.app.robot.numExplosion + 1, 1):
                if not (0 <= r + dr < self.app.numCol): break
                nextObject = self.app.objectBoard[r + dr][c]
                if isinstance(nextObject, Wall): break
                self.app.objectBoard[r + dr][c] = Explosion(self.app, self.app.getXY(r + dr, c))
                if isinstance(nextObject, Brick): break
            # explosion center
            self.app.objectBoard[r][c] = Explosion(self.app, self.app.getXY(r, c))
            self.app.robot.numBomb += 1
            return None
        self.time -= 1