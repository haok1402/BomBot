block = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]]


# Depth-First (Graph)
class Graph:
    def __init__(self):
        self.table = {}

    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = {}
        if nodeB not in self.table:
            self.table[nodeB] = {}
        self.table[nodeA][nodeB] = weight
        self.table[nodeB][nodeA] = weight

    def getEdge(self, nodeA, nodeB):
        return self.table[nodeA][nodeB]

    def getNodes(self):
        return list(self.table)

    def getNeighbors(self, node):
        return set(self.table[node])


# Depth-First (2D List)
def generate_DFS(block, cRow, cCol, tRow, tCol, visited):
    import random
    direction = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    random.shuffle(direction)
    for dRow, dCol in direction:
        nextRow, nextCol = cRow + dRow, cCol + dCol
        if (nextRow, nextCol) == (tRow, tCol):
            visited.append((cRow, cCol))
            return visited
        if (nextRow, nextCol) in visited: continue
        if not (0 <= nextRow < len(block)): continue
        if not (0 <= nextCol < len(block[0])): continue
        if not (block[nextRow][nextCol] == 0): continue
        visited.append((cRow, cCol))
        solution = generate_DFS(block, nextRow, nextCol, tRow, tCol, visited)
        if solution: return visited
        visited.pop()
    return None


def density_DFS():
    import json
    idx, density = 0, {}
    while idx <= 1000:
        path = generate_DFS(block, 1, 1, 6, 9, list())
        if len(path) not in density:
            density[len(path)] = 1
        else:
            density[len(path)] += 1
        print(f"{idx}: {len(path)}")
        idx += 1
    with open("Depth-First PathLength Distribution.json", "w") as f:
        json.dump(density, f)


def visualize_DFS():
    import json, numpy, seaborn
    data, density = json.load(open("Depth-First PathLength Distribution.json")), []
    for key in data: density += [int(key)] * data[key]
    seaborn.set_style('whitegrid')
    seaborn.kdeplot(numpy.array(density)).figure.savefig("Depth-First PathLength Distribution.png")


path = generate_DFS(block)
