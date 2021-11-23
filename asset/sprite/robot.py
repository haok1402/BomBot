import pygame

from asset.sprite.bomb import Bomb
from asset.sprite.explosion import Explosion
from asset.sprite.shoe import Shoe
from asset.sprite.potion import Potion
from asset.sprite.lightening import Lightening

ROBOT_IMG = pygame.transform.scale(pygame.image.load("./asset/image/robot-1.png").convert_alpha(), (70, 70))


class Robot(pygame.sprite.Sprite):
    def __init__(self, app, position):
        super(Robot, self).__init__()
        self.app = app
        self.image = ROBOT_IMG
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.numBomb = 1
        self.numExplosion = 1
        self.velocity = 1

    def move(self):
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rect.move_ip(0, -self.velocity)
            other = self.app.objectBoard[r - 1][c]
            if isinstance(other, Shoe):
                self.velocity += 0.5
                self.app.objectBoard[r - 1][c] = None
                return
            if isinstance(other, Potion):
                self.numExplosion += 1
                self.app.objectBoard[r - 1][c] = None
                return
            if isinstance(other, Lightening):
                self.numBomb += 1
                self.app.objectBoard[r - 1][c] = None
                return
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(0, +self.velocity)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rect.move_ip(0, +self.velocity)
            other = self.app.objectBoard[r + 1][c]
            if isinstance(other, Shoe):
                self.velocity += 0.5
                self.app.objectBoard[r + 1][c] = None
                return
            if isinstance(other, Potion):
                self.numExplosion += 1
                self.app.objectBoard[r + 1][c] = None
                return
            if isinstance(other, Lightening):
                self.numBomb += 1
                self.app.objectBoard[r + 1][c] = None
                return
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(0, -self.velocity)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.move_ip(-self.velocity, 0)
            other = self.app.objectBoard[r][c - 1]
            if isinstance(other, Shoe):
                self.velocity += 0.5
                self.app.objectBoard[r][c - 1] = None
                return
            if isinstance(other, Potion):
                self.numExplosion += 1
                self.app.objectBoard[r][c - 1] = None
                return
            if isinstance(other, Lightening):
                self.numBomb += 1
                self.app.objectBoard[r][c - 1] = None
                return
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(+self.velocity, 0)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.move_ip(+self.velocity, 0)
            other = self.app.objectBoard[r][c + 1]
            if isinstance(other, Shoe):
                self.velocity += 0.5
                self.app.objectBoard[r][c + 1] = None
                return
            if isinstance(other, Potion):
                self.numExplosion += 1
                self.app.objectBoard[r][c + 1] = None
                return
            if isinstance(other, Lightening):
                self.numBomb += 1
                self.app.objectBoard[r][c + 1] = None
                return
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(-self.velocity, 0)

    def bomb(self):
        if self.numBomb and pygame.key.get_pressed()[pygame.K_SPACE]:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            if not self.app.objectBoard[r][c]:
                self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c), self)
                self.numBomb -= 1
