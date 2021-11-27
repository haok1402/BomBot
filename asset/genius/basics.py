def constructGraph(board):
    graph = {}
    for r in range(len(board)):
        for c in range(len(board[0])):
            if not board[r][c]: continue
            if (r, c) not in graph: graph[(r, c)] = dict()
            for dr, dc in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                if not 0 <= r + dr < len(board): continue
                if not 0 <= c + dc < len(board): continue
                if board[r + dr][c + dc]: graph[(r, c)][(r + dr, c + dc)] = 1
    return graph


def constructPath(graph):
    path = {}
    for key in graph:
        path[key] = {"distance": float("inf"), "previous": None}
    return path


def dijkstra(graph, path, sNode, eNode):
    # initialize dijkstra
    unvisited = set(key for key in path)
    path[sNode]['distance'] = 0
    # find nextNodeToVisit
    def NextNodeToVisit():
        minDistance, minNode = float("inf"), None
        for node in unvisited:
            if path[node]['distance'] < minDistance:
                minDistance = path[node]['distance']
                minNode = node
        return minNode
    # implement dijkstra
    while unvisited:
        node = NextNodeToVisit()
        for neighbor in graph[node]:
            distance = path[node]['distance'] + graph[node][neighbor]
            if distance < path[neighbor]['distance']:
                path[neighbor]['distance'] = distance
                path[neighbor]['previous'] = node
        unvisited.remove(node)
    # return route
    node, route = eNode, []
    while node:
        route.append(node)
        node = path[node]['previous']
    return route


board = [[1, 1, 1, 1],
         [1, 0, 1, 0],
         [0, 1, 1, 1],
         [0, 1, 0, 0]]
graph = constructGraph(board)
path = constructPath(graph)
route = dijkstra(graph, path, (0, 0), (3, 1))
print(route)
