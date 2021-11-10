import pygame


class Floor:
    def __init__(self, app, position):
        self.app = app
        self.image = pygame.image.load("./asset/image/floor.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)


class Wall:
    def __init__(self, app, position):
        self.app = app
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/wall.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)


class Brick:
    def __init__(self, app, position):
        self.app = app
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/grape.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)


class Bomb:
    def __init__(self, app, position):
        self.app = app
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/bomb.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.time = 1000

    def detonate(self):
        if not self.time:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            # explosion leftward
            for dc in range(-1, -self.app.robot.numExplosion - 1, -1):
                if not (0 <= c + dc < self.app.numCol): break
                if isinstance(self.app.objectBoard[r][c + dc], Brick or Wall): break
                self.app.objectBoard[r][c + dc] = Explosion(self.app, self.app.getXY(r, c + dc))
            # explosion upward
            for dr in range(-1, -self.app.robot.numExplosion - 1, -1):
                if not (0 <= r + dr < self.app.numCol): break
                if isinstance(self.app.objectBoard[r + dr][c], Brick or Wall): break
                self.app.objectBoard[r + dr][c] = Explosion(self.app, self.app.getXY(r + dr, c))
            # explosion rightward
            for dc in range(1, +self.app.robot.numExplosion + 1, 1):
                if not (0 <= c + dc < self.app.numCol): break
                if isinstance(self.app.objectBoard[r][c + dc], Brick or Wall): break
                self.app.objectBoard[r][c + dc] = Explosion(self.app, self.app.getXY(r, c + dc))            # explosion downward
            # explosion downward
            for dr in range(1, +self.app.robot.numExplosion + 1, 1):
                if not (0 <= r + dr < self.app.numCol): break
                if isinstance(self.app.objectBoard[r + dr][c], Brick or Wall): break
                self.app.objectBoard[r + dr][c] = Explosion(self.app, self.app.getXY(r + dr, c))
            # explosion center
            self.app.objectBoard[r][c] = Explosion(self.app, self.app.getXY(r, c))
            self.app.robot.numBomb += 1
            return None
        self.time -= 1


class Explosion:
    def __init__(self, app, position):
        self.app = app
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/explosion.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.time = 500

    def burn(self):
        if not self.time:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            self.app.objectBoard[r][c] = None
            return None
        self.time -= 1


class Robot:
    def __init__(self, app, position):
        self.app = app
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/robot.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.isAlive = True
        self.numBomb = 1
        self.numExplosion = 2

    def move(self):
        if self.isAlive:
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.rect.move_ip(0, -1)
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.rect.move_ip(0, +1)
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.rect.move_ip(-1, 0)
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.rect.move_ip(+1, 0)

    def bomb(self):
        if self.numBomb and pygame.key.get_pressed()[pygame.K_SPACE]:
            r, c = self.app.getRC(self.rect.centerx, self.rect.centery)
            if not self.app.objectBoard[r][c]:
                self.app.objectBoard[r][c] = Bomb(self.app, self.app.getXY(r, c))
                self.numBomb -= 1


class App:
    def __init__(self):
        # configure canvas
        self.canvas = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN)
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

    def __iter__(self):
        for r in range(self.numRow):
            for c in range(self.numCol):
                yield r, c, self.positionBoard[r][c], self.objectBoard[r][c]

    def generateBoard(self):
        for r, c, pos, obj in self:
            # generate boundary Wall
            if r == 0 or r == self.numRow - 1: self.objectBoard[r][c] = Wall(self, pos)
            if c == 0 or c == self.numCol - 1: self.objectBoard[r][c] = Wall(self, pos)
            # generate centralized Brick
            if r == 7 and c != 0 and c != self.numCol - 1: self.objectBoard[r][c] = Brick(self, pos)
            if c == 10 and r != 0 and r != self.numRow - 1: self.objectBoard[r][c] = Brick(self, pos)

    def getRC(self, x: int, y: int) -> tuple:
        r, c = (y - 15) // 70, (x - 310) // 70
        return r, c

    def getXY(self, r: int, c: int) -> tuple:
        x, y = self.positionBoard[r][c]
        return x, y

    def update(self):
        self.robot.move()
        self.robot.bomb()
        for r, c, pos, obj in self:
            if isinstance(obj, Bomb): obj.detonate()
            if isinstance(obj, Explosion): obj.burn()

    def draw(self):
        self.canvas.blit(self.floor.image, self.floor.rect)
        for r, c, pos, obj in self:
            if obj: self.canvas.blit(obj.image, obj.rect)
        self.canvas.blit(self.robot.image, self.robot.rect)
        pygame.display.flip()


def main():
    # initialize
    pygame.init()
    app, run = App(), True
    # mainloop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        app.draw()
        app.update()
    # terminate
    pygame.quit()


if __name__ == "__main__":
    main()
