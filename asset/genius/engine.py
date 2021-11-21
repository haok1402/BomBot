from asset.sprite.wall import Wall
from asset.sprite.brick import Brick
from asset.sprite.bomb import Bomb


class Engine:
    def __init__(self):
        self.graph = dict()
        self.path = dict()
        self.nodeA = None

    def construct(self, board, mode):
        self.graph = dict()
        # construct (x1, y1)
        for x1 in range(len(board)):
            for y1 in range(len(board[0])):
                # in survive mode, construct (None) to graph
                if mode == "survive" and board[x1][y1]: continue
                # in normal mode, construct (None & Brick) to graph
                if isinstance(board[x1][y1], Wall): continue
                if isinstance(board[x1][y1], Bomb): continue
                if (x1, y1) not in self.graph: self.graph[(x1, y1)] = dict()
                # construct (x2, y2)
                for (dx, dy) in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                    x2, y2 = x1 + dx, y1 + dy
                    if not 0 <= x2 < len(board): continue
                    if not 0 <= y2 < len(board[0]): continue
                    if mode == "survive" and board[x2][y2]: continue
                    if isinstance(board[x2][y2], Wall): continue
                    if isinstance(board[x2][y2], Bomb): continue
                    if (x2, y2) not in self.graph: self.graph[(x2, y2)] = dict()
                    # assign weight
                    if not board[x1][y1]: self.graph[(x2, y2)][(x1, y1)] = 0
                    if not board[x2][y2]: self.graph[(x1, y1)][(x2, y2)] = 0
                    if isinstance(board[x1][y1], Brick): self.graph[(x2, y2)][(x1, y1)] = 500
                    if isinstance(board[x2][y2], Brick): self.graph[(x1, y1)][(x2, y2)] = 500

    # I use https://www.youtube.com/watch?v=pVfj6mxhdMw to understand dijkstra
    def dijkstra(self, nodeA, nodeB):

        def nextNode():
            minNode, minDistance = None, float("inf")
            for currentNode in unvisited:
                currentDistance = self.path[currentNode]["distance"]
                if currentDistance < minDistance:
                    minNode, minDistance = currentNode, currentDistance
            return minNode if minNode else next(iter(unvisited))

        def updatePath():
            currentNode = nextNode()
            for neighbor in self.graph[currentNode]:
                currentDistance = self.path[currentNode]["distance"] + self.graph[currentNode][neighbor]
                if currentDistance < self.path[neighbor]["distance"]:
                    self.path[neighbor]["distance"] = currentDistance
                    self.path[neighbor]["previous"] = currentNode
            unvisited.remove(currentNode)
            visited.add(currentNode)

        def getPath():
            path, node = [], nodeB
            while node:
                path.append(node)
                node = self.path[node]["previous"]
            path = path if len(path) != 1 else []
            return path

        # if starting node is the same, skip dijkstra and return path
        if nodeA != self.nodeA:
            unvisited, visited = set(), set()
            for key in self.graph:
                self.path[key] = {"distance": float("inf"), "previous": None}
                unvisited.add(key)
            self.path[nodeA]["distance"] = 0
            while unvisited: updatePath()
            self.nodeA = nodeA
        return getPath()
