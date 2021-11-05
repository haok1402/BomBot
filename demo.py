import pygame


class App:
    def __init__(self):
        # specify dimensions used in display
        self.width, self.height = pygame.display.get_window_size()
        self.leftMargin, self.rightMargin = 280, 40
        self.topMargin, self.bottomMargin = 40, 40
        self.gridWidth = self.gridHeight = 100
        # store position of each object on board
        self.board = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                      ['w', 'p', 'f', 'f', 'f', 'w', 'f', 'w', 'f', 'f', 'w', 'w', 'w', 'f', 'f', 'w'],
                      ['w', 'f', 'w', 'w', 'f', 'f', 'f', 'w', 'f', 'f', 'f', 'w', 'f', 'f', 'w', 'w'],
                      ['w', 'f', 'w', 'f', 'f', 'f', 'f', 'f', 'f', 'w', 'f', 'f', 'f', 'f', 'f', 'w'],
                      ['w', 'f', 'f', 'f', 'w', 'f', 'w', 'w', 'w', 'w', 'f', 'w', 'w', 'f', 'f', 'w'],
                      ['w', 'f', 'w', 'f', 'f', 'f', 'f', 'f', 'w', 'f', 'f', 'f', 'w', 'f', 'w', 'w'],
                      ['w', 'f', 'f', 'f', 'w', 'f', 'f', 'f', 'w', 'f', 'w', 'f', 'w', 'f', 'f', 'w'],
                      ['w', 'f', 'w', 'f', 'w', 'f', 'w', 'f', 'f', 'f', 'w', 'f', 'f', 'f', 'f', 'w'],
                      ['w', 'f', 'f', 'f', 'w', 'f', 'w', 'f', 'w', 'f', 'f', 'f', 'w', 'w', 'f', 'w'],
                      ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']]
        self.playerCell = (1, 1)

    def getPosition(self, row, col):
        # convert from (row, col) to (x, y) in topleft
        x = self.leftMargin + self.gridWidth * col
        y = self.topMargin + self.gridHeight * row
        return x, y

    def drawBorder(self, canvas, pos):
        x0, y0 = pos
        x1, y1 = x0 + self.gridWidth, y0
        x2, y2 = x1, y1 + self.gridHeight
        x3, y3 = x2 - self.gridWidth,  y2
        pygame.draw.line(canvas, (0, 0, 0), (x0, y0), (x3, y3), width=5)
        pygame.draw.line(canvas, (0, 0, 0), (x0, y0), (x1, y1), width=5)
        pygame.draw.line(canvas, (0, 0, 0), (x1, y1), (x2, y2), width=5)
        pygame.draw.line(canvas, (0, 0, 0), (x2, y2), (x3, y3), width=5)

    def drawWall(self, canvas, pos):
        pygame.draw.rect(surface=canvas, color=(160, 104, 52), rect=(pos[0], pos[1], self.gridWidth, self.gridHeight))
        self.drawBorder(canvas, pos)

    def drawFloor(self, canvas, pos):
        pygame.draw.rect(surface=canvas, color=(34, 139, 34), rect=(pos[0], pos[1], self.gridWidth, self.gridHeight))
        self.drawBorder(canvas, pos)

    def drawPlayer(self, canvas, pos):
        pygame.draw.rect(surface=canvas, color=(0, 0, 255), rect=(pos[0], pos[1], self.gridWidth, self.gridHeight))
        self.drawBorder(canvas, pos)

    def draw(self, canvas):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == "w":
                    self.drawWall(canvas, self.getPosition(row, col))
                elif self.board[row][col] == "f":
                    self.drawFloor(canvas, self.getPosition(row, col))
                elif self.board[row][col] == "p":
                    self.drawPlayer(canvas, self.getPosition(row, col))

    def movePlayer(self, direction):
        currRow, currCol = self.playerCell[0], self.playerCell[1]
        tempRow, tempCol = (currRow + direction[0], currCol + direction[1])
        if self.board[tempRow][tempCol] == "f":
            self.board[currRow][currCol] = "f"
            self.board[tempRow][tempCol] = "p"
            self.playerCell = (tempRow, tempCol)

    def update(self):
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_LEFT]:
            self.movePlayer(direction=(0, -1))
        elif keyPressed[pygame.K_RIGHT]:
            self.movePlayer(direction=(0, +1))
        elif keyPressed[pygame.K_DOWN]:
            self.movePlayer(direction=(+1, 0))
        elif keyPressed[pygame.K_UP]:
            self.movePlayer(direction=(-1, 0))


def appStarted():
    canvas = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN)
    pygame.display.set_caption("BomBot")
    pygame.mouse.set_visible(False)
    return App(), canvas


def captureEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: return False
    return True


def updateObject(app):
    app.update()


def updateCanvas(app, canvas):
    app.draw(canvas)
    pygame.display.flip()
    pygame.time.Clock().tick(15)


def main():
    # initialize
    pygame.init()
    (app, canvas), appRunning = appStarted(), True
    # mainloop
    while appRunning:
        appRunning = captureEvent()
        updateObject(app)
        updateCanvas(app, canvas)
    # terminate
    pygame.quit()


if __name__ == "__main__":
    main()
