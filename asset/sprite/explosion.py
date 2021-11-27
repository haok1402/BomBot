import pygame

EXPLOSION_IMG = pygame.transform.scale(pygame.image.load("./asset/image/explosion.png").convert_alpha(), (70, 70))


class Explosion:
    def __init__(self, app, position, product):
        self.app = app
        self.image = EXPLOSION_IMG
        self.rect = self.image.get_rect(center=position)
        self.product = product
        self.time = 250

    def burn(self):
        if not self.time:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            self.app.objectBoard[r][c] = self.product
            return None
        # kill robot if explosion hits
        for robot in self.app.robot:
            cx, cy = robot.rect.center
            if (self.rect.left <= cx <= self.rect.right) and (self.rect.top <= cy <= self.rect.bottom):
                robot.isAlive = False
        for enemy in self.app.enemy:
            ex, ey = enemy.rect.center
            if (self.rect.left <= ex <= self.rect.right) and (self.rect.top <= ey <= self.rect.bottom):
                enemy.isAlive = False
        self.time -= 1
