# BomBot

- Term Project for 15-112 (F21) at CMU
- BomBot Designed with PyGame

![Preview](./asset/image/preview.png)

## Sprites

### Robot

- controlled by the user
- move in four directions: left, up, right, down
- place bomb

### Enemy

- behave similar to Robot but try to kill robot

### Brick

- destructible by Explosion

### Wall

- non-destructible by Explosion

### Bomb

- once detonated, create Explosion

### Explosion

- vertical and horizontal
- kill Robot and Enemy
- does not penetrate through Brick or Wall

## Controls

Below is a list containing all controls used in BomBot.

### Position

- Move Robot: Arrows

### Bomb

- Drop Bomb: Space

## Game AI

### Shortest-Path Finding

- Dijkstra
  - mode="normal"
    - assign weight=0 for Floor
    - assign weight=500 for Brick
      - account for time-loss due to bombing Brick
    - Wall, Bomb, Explosion are removed from Graph
    - len(graph) around 195
  - mode="survive"
    - Wall, Brick, Bomb, Explosion are removed from Graph
    - path to safety doesn't require bombing any Brick
    - len(graph) around 140

### Check Safety

- if in dangerous mode:
  - move to somewhere safe
  - stay in that place until bomb is detonated

### Bomb Robot

- find the shortest path to Robot

- bomb Brick along the path
- reach Robot and BomBot

## Known Issues

### Board Generation:
  - by chance, large amount of emptiness in one location
  - by chance, robot is directly connected to other enemies without bombing bricks
  - by chance, large amount of bricks in one location
  - by chance, useless wall created (robot cannot enter space in between walls for shelter)
