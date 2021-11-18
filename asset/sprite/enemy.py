import pygame

from asset.sprite.bomb import Bomb
from asset.sprite.explosion import Explosion
from asset.genius.dijkstra import Graph

ENEMY_IMG = pygame.transform.scale(pygame.image.load("./asset/image/robot-2.png").convert_alpha(), (70, 70))


class Enemy:
    def __init__(self, app, position):
        self.app = app
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.numBomb = 1
        self.numExplosion = 2
        self.velocity = 2
        self.route = []

    def path(self):
        g = Graph(self.app.objectBoard)
        if self.app.getRC(self.rect.centerx, self.rect.centery) == (13, 1):
            return [self.app.getXY(cor[0], cor[1]) for cor in g.Dijkstra(sNode=(13, 1), eNode=(9, 5))]
        if self.app.getRC(self.rect.centerx, self.rect.centery) == (9, 5):
            return [self.app.getXY(cor[0], cor[1]) for cor in g.Dijkstra(sNode=(9, 5), eNode=(13, 1))]

    def bomb(self):
        if self.numBomb:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            if self.app.objectBoard[r][c]: return
            self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c), self)
            self.numBomb -= 1

    def automate(self):
        if not self.route:
            path = self.path()
            if not path: return
            self.route = path
        if self.rect.centerx < self.route[-1][0]:
            self.rect.move_ip(+1, 0)
        if self.rect.centerx > self.route[-1][0]:
            self.rect.move_ip(-1, 0)
        if self.rect.centery < self.route[-1][1]:
            self.rect.move_ip(0, +1)
        if self.rect.centery > self.route[-1][1]:
            self.rect.move_ip(0, -1)
        if self.rect.center == self.route[-1]: self.route.pop()
