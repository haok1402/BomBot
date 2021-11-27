# import external dependencies
import pygame
import random

# import internal dependencies
from asset.sprite.wall import Wall
from asset.sprite.brick import Brick
from asset.sprite.bomb import Bomb
from asset.sprite.explosion import Explosion
from asset.genius.engine import Engine
from asset.sprite.shoe import Shoe
from asset.sprite.potion import Potion
from asset.sprite.lightening import Lightening


class Enemy:
    def __init__(self, app, position, serial):
        self.app = app
        self.serial = serial
        self.image = pygame.transform.scale(pygame.image.load(f"./asset/image/robot-{self.serial}.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.numBomb = 1
        self.numExplosion = 1
        self.velocity = 1
        self.vision = Engine()
        self.route = []
        self.flee = False
        self.awaiting = 0

    def bomb(self):
        if self.numBomb > 0:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c), self)
            self.numBomb -= 1

    def automate(self):
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        if self.flee:
            self.move(self.route)
            if self.awaiting: self.awaiting -= 1; return
            else: self.flee = False
        if (r, c) not in self.app.dangerZone:
            if not self.route:
                self.vision.construct(board=self.app.objectBoard, exclude=self.app.dangerZone | self.app.wallZone)
                self.route = [self.app.getXY(r, c) for r, c in self.vision.dijkstra(nodeA=(r, c), nodeB=random.sample(self.app.emptyZone, 1)[0])]
            if self.route: self.move(self.route)
        if (r, c) in self.app.dangerZone:
            nearbyDangerZone = set()
            # nearbyDangerZone leftward
            for dc in range(-1, -5, -1):
                if not (0 <= c + dc < self.app.numCol): break
                nextObject = self.app.objectBoard[r][c + dc]
                if isinstance(nextObject, Wall) or isinstance(nextObject, Brick) or isinstance(nextObject, Explosion): break
                if not nextObject: nearbyDangerZone.add((r, c + dc))
            # nearbyDangerZone upward
            for dr in range(-1, -5, -1):
                if not (0 <= r + dr < self.app.numCol): break
                nextObject = self.app.objectBoard[r + dr][c]
                if isinstance(nextObject, Wall) or isinstance(nextObject, Brick) or isinstance(nextObject, Explosion): break
                if not nextObject: nearbyDangerZone.add((r + dr, c))
            # nearbyDangerZone rightward
            for dc in range(1, +5, 1):
                if not (0 <= c + dc < self.app.numCol): break
                nextObject = self.app.objectBoard[r][c + dc]
                if isinstance(nextObject, Wall) or isinstance(nextObject, Brick) or isinstance(nextObject, Explosion): break
                if not nextObject: nearbyDangerZone.add((r, c + dc))
            # nearbyDangerZone downward
            for dr in range(1, +5, 1):
                if not (0 <= r + dr < self.app.numCol): break
                nextObject = self.app.objectBoard[r + dr][c]
                if isinstance(nextObject, Wall) or isinstance(nextObject, Brick) or isinstance(nextObject, Explosion): break
                if not nextObject: nearbyDangerZone.add((r + dr, c))
            # nearbyDangerZone center
            nearbyDangerZone.add((r, c))
            # compute path
            self.vision.construct(board=self.app.objectBoard, exclude=self.app.wallZone | self.app.brickZone | self.app.dangerZone - nearbyDangerZone)
            route = []
            while not route: route = self.vision.dijkstra(nodeA=(r, c), nodeB=random.sample(self.app.emptyZone - self.app.dangerZone, 1)[0])
            self.route = [self.app.getXY(r, c) for r, c in route]
            self.flee, self.awaiting = True, 500 + 250

    def move(self, route: list):
        # remove visited route
        if not self.route: return
        if self.rect.center == route[-1]: route.pop()
        if not self.route: return
        # clear Brick in route
        brickX, brickY = route[-1]
        brickR, brickC = self.app.getRC(brickX, brickY)
        if isinstance(self.app.objectBoard[brickR][brickC], Brick): self.bomb()
        r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
        # move according to route
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

        if self.rect.centerx < route[-1][0]: move_right(); return
        if self.rect.centerx > route[-1][0]: move_left(); return
        if self.rect.centery < route[-1][1]: move_down(); return
        if self.rect.centery > route[-1][1]: move_up(); return
