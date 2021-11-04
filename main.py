import pygame


class Board:
    def __init__(self, dimension):
        self.row, self.col = dimension
        self.margin = 50

    def drawGrid(self, canvas):
        startX, endX = 5 * self.margin, canvas.get_width() - self.margin
        deltaX = deltaY = (endX - startX) / self.col
        startY, endY = self.margin, self.margin + deltaY * self.row
        for idx in range(0, self.row + 1):
            lineY = startY + idx * deltaY
            pygame.draw.line(canvas, color=(238, 232, 170), start_pos=(startX, lineY), end_pos=(endX, lineY), width=5)
        for jdx in range(0, self.col + 1):
            lineX = startX + jdx * deltaX
            pygame.draw.line(canvas, color=(238, 232, 170), start_pos=(lineX, startY), end_pos=(lineX, endY), width=5)

    def draw(self, canvas):
        self.drawGrid(canvas)


class Wall:
    def __init__(self, cell):
        self.row, self.col = cell

    def update(self):
        pass


class Player:
    def __init__(self, position):
        self.position = position
        self.velocity = 1

    def move(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_UP]:
            self.position = (self.position[0], self.position[1] - self.velocity)
        elif keyPressed[pygame.K_DOWN]:
            self.position = (self.position[0], self.position[1] + self.velocity)
        elif keyPressed[pygame.K_LEFT]:
            self.position = (self.position[0] - self.velocity, self.position[1])
        elif keyPressed[pygame.K_RIGHT]:
            self.position = (self.position[0] + self.velocity, self.position[1])

    def update(self):
        self.move()

    def draw(self, canvas):
        pygame.draw.circle(canvas, color=(000, 000, 255), center=self.position, radius=25)


class App:
    def __init__(self):
        self.board = Board(dimension=(10, 16))
        self.player = Player(position=(300, 100))

    def update(self):
        self.player.update()

    def draw(self, canvas):
        self.board.draw(canvas)
        self.player.draw(canvas)


def appStarted():
    canvas = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN)
    pygame.display.set_caption("BomBot")
    pygame.mouse.set_visible(False)
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
    pygame.display.update()


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
