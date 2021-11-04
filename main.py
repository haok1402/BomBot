import pygame


class Player:
    def __init__(self, pos=(100, 100)):
        self.pos = pos
        self.vel = 1

    def move(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_UP]:
            self.pos = (self.pos[0], self.pos[1] - self.vel)
        elif keyPressed[pygame.K_DOWN]:
            self.pos = (self.pos[0], self.pos[1] + self.vel)
        elif keyPressed[pygame.K_LEFT]:
            self.pos = (self.pos[0] - self.vel, self.pos[1])
        elif keyPressed[pygame.K_RIGHT]:
            self.pos = (self.pos[0] + self.vel, self.pos[1])

    def update(self):
        self.move()

    def draw(self, canvas):
        pygame.draw.circle(canvas, color=(0, 0, 255), center=self.pos, radius=25)


class App:
    def __init__(self):
        self.player = Player()

    def update(self):
        self.player.update()

    def draw(self, canvas):
        self.player.draw(canvas)


def appStarted():
    canvas = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN)
    pygame.display.set_caption("BomBot")
    return App(), canvas


def captureEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: return False
    return True


def updateObject(app, canvas):
    app.update()


def updateCanvas(app, canvas):
    canvas.fill(color=(0, 0, 0))
    app.draw(canvas)
    pygame.display.flip()


def main():
    # initialize
    pygame.init()
    (app, canvas), run = appStarted(), True
    # mainloop
    while run:
        run = captureEvent()
        updateObject(app, canvas)
        updateCanvas(app, canvas)
    # terminate
    pygame.quit()


if __name__ == "__main__":
    main()
