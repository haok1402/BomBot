import pygame
import random

# initialize
pygame.init()
canvas = pygame.display.set_mode(size=(1920, 1080), flags=pygame.FULLSCREEN)

from asset.floor import Floor
from asset.wall import Wall
from asset.brick import Brick
from asset.bomb import Bomb
from asset.explosion import Explosion
from asset.over import Over
from asset.robot import Robot
from asset.enemy import Enemy


class App:
    def __init__(self):
        # configure canvas
        self.canvas = canvas
        pygame.display.set_caption("BomBot")
        # configure mouse
        pygame.mouse.set_visible(False)
        # configure game
        self.isGameOver = False
        self.numRow, self.numCol = 15, 21
        self.positionBoard = [[(c + 35, r + 35) for c in range(310, 1780, 70)] for r in range(15, 1065, 70)]
        self.objectBoard = [[None for c in range(self.numCol)] for _ in range(self.numRow)]
        self.generateBoard()
        # configure sprite
        self.floor = Floor(self, (310, 15))
        self.robot = Robot(self, self.positionBoard[1][1])
        self.over = Over(self, position=(1045, 540))
        self.enemy = [Enemy(self, self.positionBoard[13][1], 1),
                      Enemy(self, self.positionBoard[1][19], 2),
                      Enemy(self, self.positionBoard[13][19], 3)]

    def __iter__(self):
        for r in range(self.numRow):
            for c in range(self.numCol):
                yield r, c, self.positionBoard[r][c], self.objectBoard[r][c]

    def generateBoard(self):
        for r, c, pos, obj in self:
            # generate randomized Brick
            num = random.random()
            if 0.0 <= num < 0.4: self.objectBoard[r][c] = None
            if 0.5 <= num < 0.8: self.objectBoard[r][c] = Brick(self, pos)
            if 0.8 <= num < 1.0: self.objectBoard[r][c] = Wall(self, pos)
            # generate boundary Wall
            if r == 0 or r == self.numRow - 1: self.objectBoard[r][c] = Wall(self, pos)
            if c == 0 or c == self.numCol - 1: self.objectBoard[r][c] = Wall(self, pos)
            # generate space Robot
            if (r, c) == (1, 1) or (r, c) == (1, 2) or (r, c) == (2, 1): self.objectBoard[r][c] = None
            if (r, c) == (13, 1) or (r, c) == (12, 1) or (r, c) == (13, 2): self.objectBoard[r][c] = None
            if (r, c) == (1, 19) or (r, c) == (2, 19) or (r, c) == (1, 18): self.objectBoard[r][c] = None
            if (r, c) == (13, 19) or (r, c) == (12, 19) or (r, c) == (13, 18): self.objectBoard[r][c] = None

    def getRC(self, x: int, y: int) -> tuple:
        r, c = (y - 15) // 70, (x - 310) // 70
        return r, c

    def getXY(self, r: int, c: int) -> tuple:
        x, y = self.positionBoard[r][c]
        return x, y

    def detectCollision(self, object01, object02):
        if not (object01 and object02): return None
        # capture (x, y) for object01 and object02
        (x1, y1), (x2, y2) = object01.rect.topleft, object01.rect.bottomright
        (x3, y3), (x4, y4) = object02.rect.topleft, object02.rect.bottomright
        # object02 collides object01 from bottom-right
        if (x1 <= x3 <= x2) and (y1 <= y3 <= y2): return object02
        # object02 collides object01 from bottom-left
        if (x1 <= x4 <= x2) and (y1 <= y3 <= y2): return object02
        # object02 collides object01 from top-right
        if (x1 <= x3 <= x2) and (y1 <= y4 <= y2): return object02
        # object02 collides object01 from top-left
        if (x1 <= x4 <= x2) and (y1 <= y4 <= y2): return object02
        # no collision detected
        return None

    def update(self):
        if self.robot.isAlive:
            self.robot.move()
            self.robot.bomb()
            for r, c, pos, obj in self:
                if isinstance(obj, Bomb): obj.detonate()
                if isinstance(obj, Explosion): obj.burn()

    def draw(self):
        self.canvas.blit(self.floor.image, self.floor.rect)
        for r, c, pos, obj in self:
            if obj: self.canvas.blit(obj.image, obj.rect)
        for enemy in self.enemy:
            self.canvas.blit(enemy.image, enemy.rect)
            if not enemy.isAlive: self.enemy.remove(enemy)
        self.canvas.blit(self.robot.image, self.robot.rect)
        if not self.robot.isAlive: self.canvas.blit(self.over.image, self.over.rect)
        pygame.display.flip()


def main():
    app, run = App(), True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        app.draw()
        app.update()
    pygame.quit()


if __name__ == "__main__":
    main()
