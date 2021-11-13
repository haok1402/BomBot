import pygame

from explosion import Explosion
from bomb import Bomb

ROBOT_IMG = pygame.transform.scale(pygame.image.load("./asset/image/robot-1.png").convert_alpha(), (70, 70))


class Robot:
    def __init__(self, app, position):
        self.app = app
        self.image = ROBOT_IMG
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.numBomb = 1
        self.numExplosion = 2
        self.velocity = 2

    def move(self):
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rect.move_ip(0, -self.velocity)
            # undo move if collision detected
            collision = self.app.detectCollision(self, self.app.objectBoard[r - 1][c])
            if collision and not isinstance(collision, Explosion): self.rect.move_ip(0, +self.velocity)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rect.move_ip(0, +self.velocity)
            # undo move if collision detected
            collision = self.app.detectCollision(self, self.app.objectBoard[r + 1][c])
            if collision and not isinstance(collision, Explosion): self.rect.move_ip(0, -self.velocity)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.move_ip(-self.velocity, 0)
            # undo move if collision detected
            collision = self.app.detectCollision(self, self.app.objectBoard[r][c - 1])
            if collision and not isinstance(collision, Explosion): self.rect.move_ip(+self.velocity, 0)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.move_ip(+self.velocity, 0)
            # undo move if collision detected
            collision = self.app.detectCollision(self, self.app.objectBoard[r][c + 1])
            if collision and not isinstance(collision, Explosion): self.rect.move_ip(-self.velocity, 0)

    def bomb(self):
        if self.numBomb and pygame.key.get_pressed()[pygame.K_SPACE]:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            if not self.app.objectBoard[r][c]:
                self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c))
                self.numBomb -= 1
