class Graph:
    def __init__(self):
        self.graph = {"A": {"B": 6, "D": 1},
                      "B": {"C": 5},
                      "C": {},
                      "D": {"B": 2, "E": 1},
                      "E": {"B": 2, "C": 5}}
        self.path = {"A": {"distance": float("inf"), "previous": None},
                     "B": {"distance": float("inf"), "previous": None},
                     "C": {"distance": float("inf"), "previous": None},
                     "D": {"distance": float("inf"), "previous": None},
                     "E": {"distance": float("inf"), "previous": None}}
        self.unvisited, self.visited = {"A", "B", "C", "D", "E"}, set()

    def Dijkstra(self, sNode, eNode):

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

        self.path[sNode]["distance"] = 0
        while self.unvisited: UpdatePath()
        return GetPath()


g = Graph()
AtoC = g.Dijkstra(sNode="A", eNode="C")
print(AtoC)
