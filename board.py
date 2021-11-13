import random
import seaborn
import numpy

"""
Different Blocks
"""
# L = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
#
# block01 = [L[i][0:10] for i in range(0, 7)]
# block02 = [L[i][0:10] for i in range(8, 15)]
# block03 = [L[i][11:21] for i in range(0, 7)]
# block04 = [L[i][11:21] for i in range(8, 15)]

"""
Depth-First Search
"""
block01 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]]


def generate(block, cRow, cCol, tRow, tCol, visited):
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
        solution = generate(block, nextRow, nextCol, tRow, tCol, visited)
        if solution: return visited
        visited.pop()
    return None


while True:
    path = generate(block01, 1, 1, 6, 9, list())
    for b in block01: print(b)
    print(len(path))
