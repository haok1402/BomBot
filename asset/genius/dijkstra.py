from asset.sprite.wall import Wall
from asset.sprite.brick import Brick
from asset.sprite.bomb import Bomb


class Graph:
    def __init__(self, board, mode="normal"):
        self.mode, self.board, self.status = mode, board, False  # self.status avoids dijkstra over self.graph twice
        self.graph, self.path = dict(), dict()
        self.unvisited, self.visited = set(), set()
        self.GridToGraph()

    def GridToGraph(self):
        for x1 in range(len(self.board)):
            for y1 in range(len(self.board[0])):
                # only search for Floor with weight=0 when trying to avoid bombs
                if self.mode == "survive" and self.board[x1][y1]: continue
                # initialize (x1, y1) in graph
                if isinstance(self.board[x1][y1], Wall): continue
                if isinstance(self.board[x1][y1], Bomb): continue
                if (x1, y1) not in self.graph:
                    self.graph[(x1, y1)] = {}
                for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                    x2, y2 = x1 + dx, y1 + dy
                    # initialize (x2, y2) in graph
                    if not 0 <= x2 < len(self.board): continue
                    if not 0 <= y2 < len(self.board[0]): continue
                    # only search for Floor with weight=0 when trying to avoid bombs
                    if self.mode == "survive" and self.board[x2][y2]: continue
                    if isinstance(self.board[x2][y2], Wall): continue
                    if isinstance(self.board[x2][y2], Bomb): continue
                    if (x2, y2) not in self.graph:
                        self.graph[(x2, y2)] = {}
                    # assign weight in both directions
                    if self.board[x1][y1] is None:
                        self.graph[(x2, y2)][(x1, y1)] = 0
                    if self.board[x2][y2] is None:
                        self.graph[(x1, y1)][(x2, y2)] = 0
                    if isinstance(self.board[x1][y1], Brick):
                        self.graph[(x2, y2)][(x1, y1)] = 500
                    if isinstance(self.board[x2][y2], Brick):
                        self.graph[(x1, y1)][(x2, y2)] = 500

    def Dijkstra(self, sNode, eNode):

        def NextNode():
            minNode, minDistance = None, float("inf")
            for node in self.unvisited:
                currentDistance = self.path[node]["distance"]
                if currentDistance < minDistance:
                    minNode, minDistance = node, currentDistance
            # non-destructively retrieve an element from a set in O(1) https://stackoverflow.com/questions/59825/
            return minNode if minNode else next(iter(self.unvisited))

        def UpdatePath():
            currentNode = NextNode()
            previousDistance = self.path[currentNode]["distance"]
            for neighbor in self.graph[currentNode]:
                if self.graph[currentNode][neighbor] + previousDistance < self.path[neighbor]["distance"]:
                    self.path[neighbor]["distance"] = self.graph[currentNode][neighbor] + previousDistance
                    self.path[neighbor]["previous"] = currentNode
            self.unvisited.remove(currentNode)
            self.visited.add(currentNode)

        def GetPath():
            path, node = [], eNode
            while node:
                path.append(node)
                node = self.path[node]["previous"]
            # no path exists
            path = path if len(path) != 1 else []
            return path

        if not self.status:
            # initialize dijkstra
            self.path[sNode]["distance"] = 0
            for key in self.graph:
                self.path[key] = {"distance": float("inf"), "previous": None}
                self.unvisited.add(key)
            # execute dijkstra
            while self.unvisited: UpdatePath()
            self.status = True
        # return dijkstra's path
        return GetPath()
