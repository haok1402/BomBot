# import external dependencies
import pygame
import random

# initialize pygame
pygame.init()

# configure canvas
canvas = pygame.display.set_mode(size=(1920, 1080), flags=pygame.FULLSCREEN)
pygame.display.set_caption("BomBot")
pygame.mouse.set_visible(False)

# import internal dependencies
from asset.sprite.floor import Floor
from asset.sprite.wall import Wall
from asset.sprite.brick import Brick
from asset.sprite.bomb import Bomb
from asset.sprite.explosion import Explosion
from asset.sprite.over import Over
from asset.sprite.robot import Robot
from asset.genius.enemy import Enemy


class App:
    def __init__(self, game_mode):
        self.game_mode = game_mode
        self.canvas = canvas
        # configure BomBot
        self.isGameOver = False
        self.numRow, self.numCol = 15, 21
        self.positionBoard = [[(c + 35, r + 35) for c in range(310, 1780, 70)] for r in range(15, 1065, 70)]
        self.objectBoard = [[None for _ in range(self.numCol)] for _ in range(self.numRow)]
        self.board = self.generate_board()
        # AI Engine
        self.dangerZone = set()
        self.getDangerZone()
        self.brickZone = set()
        self.getBrickZone()
        self.wallZone = set()
        self.getWallZone()
        self.emptyZone = set()
        self.getEmptyZone()
        # configure sprite
        self.floor = Floor(self, (310, 15))
        self.over = Over(self, position=(1045, 540))
        if self.game_mode == "one_player":
            self.robot = [Robot(self, self.positionBoard[1][1], 1)]
            self.enemy = [Enemy(self, self.positionBoard[13][1], 2),
                          Enemy(self, self.positionBoard[1][19], 3),
                          Enemy(self, self.positionBoard[13][19], 4)]
        if self.game_mode == "two_player":
            self.robot = [Robot(self, self.positionBoard[1][1], 1),
                          Robot(self, self.positionBoard[13][19], 4)]
            self.enemy = [Enemy(self, self.positionBoard[13][1], 2),
                          Enemy(self, self.positionBoard[1][19], 3)]

    def __iter__(self) -> (int, int, tuple, object):
        for r in range(self.numRow):
            for c in range(self.numCol):
                yield r, c, self.positionBoard[r][c], self.objectBoard[r][c]

    def generate_board(self) -> None:
        # space reserved for robot
        s = {(1, 1), (1, 2), (2, 1), (13, 1), (12, 1), (13, 2), (1, 19), (2, 19), (1, 18), (13, 19), (12, 19), (13, 18)}
        for r, c, pos, obj in self:
            # randomized brick
            ranNum = random.random()
            if 0.0 <= ranNum < 0.3: self.objectBoard[r][c] = None
            if 0.5 <= ranNum < 0.8: self.objectBoard[r][c] = Brick(self, pos)
            if 0.8 <= ranNum < 1.0: self.objectBoard[r][c] = Wall(self, pos)
            # boundary wall
            if r == 0 or r == self.numRow - 1: self.objectBoard[r][c] = Wall(self, pos)
            if c == 0 or c == self.numCol - 1: self.objectBoard[r][c] = Wall(self, pos)
            # robot passage
            if (r, c) in s: self.objectBoard[r][c] = None

    def check_status(self) -> bool:
        game_over = True
        for robot in self.robot:
            if robot.isAlive: game_over = False
        return game_over

    def getRC(self, x: int, y: int) -> tuple:
        r, c = (y - 15) // 70, (x - 310) // 70
        return r, c

    def getXY(self, r: int, c: int) -> tuple:
        x, y = self.positionBoard[r][c]
        return x, y

    def getDangerZone(self):
        self.dangerZone = set()
        for r, c, pos, obj in self:
            if isinstance(obj, Bomb):
                self.dangerZone = self.dangerZone | obj.explode()
            if isinstance(obj, Explosion):
                self.dangerZone.add((r, c))

    def getBrickZone(self):
        self.brickZone = set()
        for r, c, pos, obj in self:
            if isinstance(obj, Brick):
                self.brickZone.add((r, c))

    def getWallZone(self):
        self.wallZone = set()
        for r, c, pos, obj in self:
            if isinstance(obj, Wall):
                self.wallZone.add((r, c))

    def getEmptyZone(self):
        self.emptyZone = set()
        for r, c, pos, obj in self:
            if not obj:
                self.emptyZone.add((r, c))

    def detectCollision(self, object01, object02):
        if not object02 or isinstance(object02, Explosion): return False
        return pygame.sprite.collide_rect(object01, object02)

    def update(self) -> None:
        self.isGameOver = self.check_status()
        if not self.isGameOver:
            for robot in self.robot:
                if robot.isAlive:
                    robot.move()
                    robot.bomb()
            for enemy in self.enemy:
                if enemy.isAlive:
                    enemy.automate()
            for r, c, pos, obj in self:
                if isinstance(obj, Bomb): obj.detonate()
                if isinstance(obj, Explosion): obj.burn()
            # AI Engine
            self.getDangerZone()
            self.getBrickZone()
            self.getEmptyZone()
            self.getWallZone()

    def draw(self) -> None:
        self.isGameOver = self.check_status()
        if not self.isGameOver:
            self.canvas.blit(self.floor.image, self.floor.rect)
            for r, c, pos, obj in self:
                 if obj: self.canvas.blit(obj.image, obj.rect)
            for enemy in self.enemy:
                self.canvas.blit(enemy.image, enemy.rect)
                if not enemy.isAlive: self.enemy.remove(enemy)
            for robot in self.robot:
                self.canvas.blit(robot.image, robot.rect)
                if not robot.isAlive: self.robot.remove(robot)
        if self.isGameOver:
            self.canvas.blit(self.over.image, self.over.rect)
        pygame.display.flip()


# select game_mode
def menu() -> str:
    selecting, selected = True, 0
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selecting = False
            # Menu Basic
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected > 0: selected -= 1
                elif event.key == pygame.K_DOWN:
                    if selected < 1: selected += 1
                # 0: one_player, 1: two_player
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        return "one_player"
                    if selected == 1:
                        return "two_player"
        # Menu Canvas
        canvas.fill((0, 0, 0))
        font = pygame.font.SysFont('Comic Sans MS', 100)
        if selected == 0:
            text_one = font.render("One Player", False, (255, 255, 0))
            pygame.draw.polygon(canvas, (255, 255, 0), [(650, 425), (650, 325), (720, 375)])
        else:
            text_one = font.render("One Player", False, (255, 255, 255))
        if selected == 1:
            text_two = font.render("Two Player", False, (255, 255, 0))
            pygame.draw.polygon(canvas, (255, 255, 0), [(650, 625), (650, 525), (720, 575)])
        else:
            text_two = font.render("Two Player", False, (255, 255, 255))
        canvas.blit(text_one, (740, 300))
        canvas.blit(text_two, (740, 500))
        pygame.display.flip()


def main():
    game_mode = menu()
    app, running = App(game_mode), True
    pygame.event.clear()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        app.draw()
        app.update()
    pygame.quit()


if __name__ == "__main__":
    main()
