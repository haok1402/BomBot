"""
CITATION:
With explanation of Dijkstra's Algorithm (https://www.youtube.com/watch?v=pVfj6mxhdMw), I created the following.
"""

class Graph:
    def __init__(self, board):
        self.board = board
        self.graph, self.path = dict(), dict()
        self.unvisited, self.visited = set(), set()

    def Dijkstra(self, sNode, eNode):

        def GridToGraph():
            for x1 in range(len(self.board)):
                for y1 in range(len(self.board)):
                    # initialize (x1, y1) in graph
                    if (x1, y1) not in self.graph: self.graph[(x1, y1)] = {}
                    for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                        x2, y2 = x1 + dx, y1 + dy
                        # check if neighbor is valid
                        if not 0 <= x2 < len(self.board): continue
                        if not 0 <= y2 < len(self.board[0]): continue
                        # initialize (x2, y2) in graph
                        if (x2, y2) not in self.graph: self.graph[(x2, y2)] = {}
                        # assign weight in both directions
                        self.graph[(x1, y1)][(x2, y2)] = self.board[x2][y2]
                        self.graph[(x2, y2)][(x1, y1)] = self.board[x1][y1]
            # initialize dijkstra
            for key in self.graph:
                self.path[key] = {"distance": float("inf"), "previous": None}
                self.unvisited.add(key)

        def NextNode():
            minNode, minDistance = "", float("inf")
            for node in self.unvisited:
                currentDistance = self.path[node]["distance"]
                if currentDistance < minDistance:
                    minNode, minDistance = node, currentDistance
            return minNode

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
            return path[::-1]

        GridToGraph()
        self.path[sNode]["distance"] = 0
        while self.unvisited: UpdatePath()
        return GetPath()


from random import randint
m = [[randint(0, 9) for _ in range(5)] for _ in range(5)]
for i in m: print(i)
g = Graph(m)
print(g.Dijkstra(sNode=(0, 0), eNode=(4, 4)))
