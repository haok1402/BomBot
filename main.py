import pygame


class Board:
    def __init__(self):
        pass

    def draw(self, canvas):
        canvas.fill((0, 0, 0))


class Bomb:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/bomb.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.time = 1000


class Explosion:
    def __init__(self, position):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/explosion.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect(center=position)
        self.time = 1000


class Robot:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("./asset/image/robot.png").convert_alpha(), (70, 70))
        self.rect = self.image.get_rect()
        self.numBomb = 1
        self.bomb = []

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

    def detonateBomb(self):
        for b in self.bomb:
            if b.time == 0:
                self.bomb.remove(b)
                self.numBomb += 1
            else: b.time -= 1

    def update(self):
        self.move()
        self.placeBomb()
        self.detonateBomb()

    def draw(self, canvas):
        for b in self.bomb:
            canvas.blit(b.image, b.rect)
        canvas.blit(self.image, self.rect)


class App:
    def __init__(self):
        self.board = Board()
        self.robot = Robot()

    def update(self):
        self.robot.update()

    def draw(self, canvas):
        self.board.draw(canvas)
        self.robot.draw(canvas)


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
