import pygame

from asset.sprite.bomb import Bomb
from asset.sprite.explosion import Explosion
from asset.sprite.shoe import Shoe
from asset.sprite.potion import Potion
from asset.sprite.lightening import Lightening


class Robot(pygame.sprite.Sprite):
    def __init__(self, app, position, serial):
        super(Robot, self).__init__()
        self.app = app
        self.serial = serial
        self.image = pygame.transform.scale(pygame.image.load(f"./asset/image/robot-{self.serial}.png").convert_alpha(),
                                            (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.numBomb = 1
        self.numExplosion = 1
        self.velocity = 1

    def move(self):
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)

        def move_up():
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

        def move_down():
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

        def move_left():
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

        def move_right():
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

        # first player
        if pygame.key.get_pressed()[pygame.K_w] and self.serial == 1: move_up()
        elif pygame.key.get_pressed()[pygame.K_s] and self.serial == 1: move_down()
        elif pygame.key.get_pressed()[pygame.K_a] and self.serial == 1: move_left()
        elif pygame.key.get_pressed()[pygame.K_d] and self.serial == 1: move_right()
        # second player
        if pygame.key.get_pressed()[pygame.K_UP] and self.serial == 4: move_up()
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.serial == 4: move_down()
        elif pygame.key.get_pressed()[pygame.K_LEFT] and self.serial == 4: move_left()
        elif pygame.key.get_pressed()[pygame.K_RIGHT] and self.serial == 4: move_right()

    def bomb(self):
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)

        def place_bomb():
            if not self.app.objectBoard[r][c]:
                self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c), self)
                self.numBomb -= 1
        # first player
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.numBomb and self.serial == 1: place_bomb()
        # second player
        if pygame.key.get_pressed()[pygame.K_RETURN] and self.numBomb and self.serial == 4: place_bomb()
