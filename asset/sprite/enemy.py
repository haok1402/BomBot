import pygame

from asset.sprite.wall import Wall
from asset.sprite.brick import Brick
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
        self.velocity = 1
        self.route = []
        self.adjacentBomb = []

    def path(self):
        g = Graph(self.app.objectBoard, "normal")
        if self.app.getRC(self.rect.centerx, self.rect.centery) == (13, 1):
            return [self.app.getXY(cor[0], cor[1]) for cor in g.Dijkstra(sNode=(13, 1), eNode=(12, 1))]
        if self.app.getRC(self.rect.centerx, self.rect.centery) == (12, 1):
            return [self.app.getXY(cor[0], cor[1]) for cor in g.Dijkstra(sNode=(12, 1), eNode=(13, 2))]
        if self.app.getRC(self.rect.centerx, self.rect.centery) == (13, 2):
            return [self.app.getXY(cor[0], cor[1]) for cor in g.Dijkstra(sNode=(13, 2), eNode=(12, 1))]

    def detectBomb(self):
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        bomb = []
        # search Bomb leftward
        for dc in range(-1, -4, -1):
            if not 0 <= c + dc < len(self.app.objectBoard[0]): continue
            other = self.app.objectBoard[r][c + dc]
            if isinstance(other, Brick): continue
            if isinstance(other, Wall): continue
            if isinstance(other, Bomb): bomb.append((r, c + dc))
        # search Bomb rightward
        for dc in range(+1, +4, +1):
            if not 0 <= c + dc < len(self.app.objectBoard[0]): continue
            other = self.app.objectBoard[r][c + dc]
            if isinstance(other, Brick): continue
            if isinstance(other, Wall): continue
            if isinstance(other, Bomb): bomb.append((r, c + dc))
        # search Bomb upward
        for dr in range(-1, -4, -1):
            if not 0 <= r + dr < len(self.app.objectBoard): continue
            other = self.app.objectBoard[r + dr][c]
            if isinstance(other, Brick): continue
            if isinstance(other, Wall): continue
            if isinstance(other, Bomb): bomb.append((r + dr, c))
        # search Bomb downward
        for dr in range(+1, +4, +1):
            if not 0 <= r + dr < len(self.app.objectBoard): continue
            other = self.app.objectBoard[r + dr][c]
            if isinstance(other, Brick): continue
            if isinstance(other, Wall): continue
            if isinstance(other, Bomb): bomb.append((r + dr, c))
        return bomb

    def avoidBomb(self):
        g = Graph(self.app.objectBoard, "survive")


    def bomb(self):
        if self.numBomb:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            if self.app.objectBoard[r][c]: return
            self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c), self)
            self.numBomb -= 1

    def automate(self):
        # check safety
        self.adjacentBomb = self.detectBomb()
        if self.adjacentBomb: self.avoidBomb()
        # find path
        if not self.route:
            path = self.path()
            if not path: return
            self.route = path
        # move accordingly
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        if self.rect.centerx < self.route[-1][0]:
            self.rect.move_ip(+self.velocity, 0)
            other = self.app.objectBoard[r][c + 1]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(-self.velocity, 0)
            return
        if self.rect.centerx > self.route[-1][0]:
            self.rect.move_ip(-self.velocity, 0)
            other = self.app.objectBoard[r][c - 1]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(+self.velocity, 0)
            return
        if self.rect.centery < self.route[-1][1]:
            self.rect.move_ip(0, +self.velocity)
            other = self.app.objectBoard[r + 1][c]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(0, -self.velocity)
            return
        if self.rect.centery > self.route[-1][1]:
            self.rect.move_ip(0, -self.velocity)
            other = self.app.objectBoard[r - 1][c]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(0, +self.velocity)
            return
        if self.rect.center == self.route[-1]: self.route.pop()
