import pygame


class Wall:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/wall.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)


class Board:
    def __init__(self, row, col):
        self.row, self.col = row, col
        # left=310, right=1780, gridWidth=70; top=15, bottom=1065, gridHeight=70;
        self.position = [[(c + 35, r + 35) for c in range(310, 1780, 70)] for r in range(15, 1065, 70)]
        self.object = [[None for r in range(self.col)] for c in range(self.row)]
        self.createBoard()

    def createBoard(self):
        for r in range(self.row):
            for c in range(self.col):
                if r == 0 or r == self.row - 1: self.object[r][c] = Wall(self.position[r][c])
                if c == 0 or c == self.col - 1: self.object[r][c] = Wall(self.position[r][c])

    def draw(self, canvas):
        canvas.fill((0, 0, 0))
        for r in range(self.row):
            for c in range(self.col):
                if self.object[r][c]: canvas.blit(self.object[r][c].image, self.object[r][c].rect)


class Bomb:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/bomb.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.time = 1000


class Explosion:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/explosion.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.time = 500


class Over:
    def __init__(self):
        self.image = pygame.image.load("./asset/image/game-over.png").convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self, canvas):
        canvas.blit(self.image, self.rect)


class Robot:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/robot.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect()
        self.numBomb = 1
        self.bomb = []
        self.explosion = []
        self.explosionDirection = [(-70 * 1, 0), (-70 * 2, 0), (+70 * 1, 0), (+70 * 2, 0),
                                   (0, -70 * 1), (0, -70 * 2), (0, +70 * 1), (0, +70 * 2), (0, 0)]
        self.isAlive = True

    def move(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_UP]:
            self.rect.move_ip(0, -1)
        elif keyPressed[pygame.K_DOWN]:
            self.rect.move_ip(0, +1)
        elif keyPressed[pygame.K_LEFT]:
            self.rect.move_ip(-1, 0)
        elif keyPressed[pygame.K_RIGHT]:
            self.rect.move_ip(+1, 0)

    def placeBomb(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_SPACE] and self.numBomb:
            self.bomb.append(Bomb(self.rect.center))
            self.numBomb -= 1

    def timeBomb(self):
        for b in self.bomb:
            if b.time == 0:
                for dX, dY in self.explosionDirection:
                    cX, cY = b.rect.center[0] + dX, b.rect.center[1] + dY
                    self.explosion.append(Explosion((cX, cY)))
                self.bomb.remove(b)
                self.numBomb += 1
            else:
                b.time -= 1

    def timeExplosion(self):
        for e in self.explosion:
            if e.time == 0:
                self.explosion.remove(e)
            else:
                e.time -= 1

    def doKill(self):
        cx, cy = self.rect.center
        for e in self.explosion:
            (x0, y0), (x1, y1) = e.rect.topleft, e.rect.bottomright
            if (x0 <= cx <= x1) and (y0 <= cy <= y1): self.isAlive = False

    def update(self):
        if self.isAlive:
            self.move()
            self.placeBomb()
            self.doKill()
            self.timeBomb()
            self.timeExplosion()

    def draw(self, canvas):
        for b in self.bomb:
            canvas.blit(b.image, b.rect)
        for e in self.explosion:
            canvas.blit(e.image, e.rect)
        canvas.blit(self.image, self.rect)


class App:
    def __init__(self):
        self.board = Board(15, 21)
        self.robot = Robot()
        self.over = Over()

    def update(self):
        self.robot.update()

    def draw(self, canvas):
        self.board.draw(canvas)
        self.robot.draw(canvas)
        if not self.robot.isAlive: self.over.draw(canvas)


def captureEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: return False
    return True


def appStarted():
    canvas = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN)
    pygame.display.set_caption("BomBot")
    pygame.mouse.set_visible(False)
    return App(), canvas


def updateObject(app):
    app.update()


def updateCanvas(app, canvas):
    app.draw(canvas)
    pygame.display.flip()


def main():
    # initialize
    app, canvas = appStarted()
    appRunning = True
    # mainloop
    while appRunning:
        appRunning = captureEvent()
        updateObject(app)
        updateCanvas(app, canvas)
    # terminate
    pygame.quit()


if __name__ == "__main__":
    main()
