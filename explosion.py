import pygame

EXPLOSION_IMG = pygame.transform.scale(pygame.image.load("./asset/image/explosion.png").convert_alpha(), (70, 70))


class Explosion:
    def __init__(self, app, position):
        self.app = app
        self.image = EXPLOSION_IMG
        self.rect = self.image.get_rect(center=position)
        self.time = 250

    def burn(self):
        if not self.time:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            self.app.objectBoard[r][c] = None
            return None
        # kill robot if explosion hits
        cx, cy = self.app.robot.rect.center
        if (self.rect.left <= cx <= self.rect.right) and (self.rect.top <= cy <= self.rect.bottom):
            self.app.robot.isAlive = False
        self.time -= 1
