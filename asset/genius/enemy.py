# import external dependencies
import pygame
import random

# import internal dependencies
from asset.sprite.wall import Wall
from asset.sprite.brick import Brick
from asset.sprite.bomb import Bomb
from asset.sprite.explosion import Explosion
from asset.genius.engine import Engine

ENEMY_IMG = pygame.transform.scale(pygame.image.load("./asset/image/robot-2.png").convert_alpha(), (70, 70))


class Enemy:
    def __init__(self, app, position):
        self.app = app
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.velocity = 1
        self.vision = Engine()
        self.vision.construct(board=self.app.objectBoard, mode="normal")
        self.routeToSafety = []
        self.timeToSafety = 0
        self.routeToRandom = []

    def move(self, route):
        if self.rect.center == route[-1]: route.pop(); return
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        if self.rect.centerx < route[-1][0]:
            self.rect.move_ip(+self.velocity, 0)
            other = self.app.objectBoard[r][c + 1]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(-self.velocity, 0); return
        if self.rect.centerx > route[-1][0]:
            self.rect.move_ip(-self.velocity, 0)
            other = self.app.objectBoard[r][c - 1]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(+self.velocity, 0); return
        if self.rect.centery < route[-1][1]:
            self.rect.move_ip(0, +self.velocity)
            other = self.app.objectBoard[r + 1][c]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(0, -self.velocity); return
        if self.rect.centery > route[-1][1]:
            self.rect.move_ip(0, -self.velocity)
            other = self.app.objectBoard[r - 1][c]
            if not other or isinstance(other, Explosion): return
            if pygame.sprite.collide_rect(self, other): self.rect.move_ip(0, +self.velocity); return


    def detectBomb(self):
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        bombDetected = []
        # search Bomb leftward
        for dc in range(-1, -4, -1):
            if not 0 <= c + dc < len(self.app.objectBoard[0]): break
            other = self.app.objectBoard[r][c + dc]
            if isinstance(other, Brick): break
            if isinstance(other, Wall): break
            if isinstance(other, Bomb): bombDetected.append(self.app.objectBoard[r][c + dc])
        # search Bomb rightward
        for dc in range(+1, +4, +1):
            if not 0 <= c + dc < len(self.app.objectBoard[0]): break
            other = self.app.objectBoard[r][c + dc]
            if isinstance(other, Brick): break
            if isinstance(other, Wall): break
            if isinstance(other, Bomb): bombDetected.append(self.app.objectBoard[r][c + dc])
        # search Bomb upward
        for dr in range(-1, -4, -1):
            if not 0 <= r + dr < len(self.app.objectBoard): break
            other = self.app.objectBoard[r + dr][c]
            if isinstance(other, Brick): break
            if isinstance(other, Wall): break
            if isinstance(other, Bomb): bombDetected.append(self.app.objectBoard[r + dr][c])
        # search Bomb downward
        for dr in range(+1, +4, +1):
            if not 0 <= r + dr < len(self.app.objectBoard): break
            other = self.app.objectBoard[r + dr][c]
            if isinstance(other, Brick): break
            if isinstance(other, Wall): break
            if isinstance(other, Bomb): bombDetected.append(self.app.objectBoard[r + dr][c])
        return bombDetected

    def avoidBomb(self, bombDetected):
        self.vision.construct(board=self.app.objectBoard, mode="survive")
        dangerZone, safetyZone = set(), set()
        # update dangerZone due to several nearby Bomb
        timeToSafety = float("inf")
        for bomb in bombDetected:
            if bomb.time < timeToSafety: timeToSafety = bomb.time
            explosionZone = bomb.explode()
            for explosion in explosionZone:
                if explosion not in dangerZone:
                    dangerZone.add(explosion)
        # find time remaining until explosion
        self.timeToSafety = timeToSafety
        # safetyZone: 1) it's free to go; 2) it's outside dangerZone
        for r in range(len(self.app.objectBoard)):
            for c in range(len(self.app.objectBoard[0])):
                other = self.app.objectBoard[r][c]
                if not other and other not in dangerZone: safetyZone.add((r, c))
        # update routeToSafety
        print("safetyZone:", safetyZone)
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        while not self.routeToSafety and safetyZone:
            nodeB = safetyZone.pop()
            routeToSafety = self.vision.dijkstra(nodeA=(r, c), nodeB=nodeB)
            if routeToSafety:
                print("nodeB", nodeB)
                print("routeToSafety:", routeToSafety)
            self.routeToSafety = [self.app.getXY(cor[0], cor[1]) for cor in routeToSafety]

    def automate(self):
        if not self.routeToSafety:
            if not self.timeToSafety:
                bombDetected = self.detectBomb()
                if bombDetected: self.avoidBomb(bombDetected)
        if self.routeToSafety:
            self.move(route=self.routeToSafety)
        if self.timeToSafety: self.timeToSafety -= 1
