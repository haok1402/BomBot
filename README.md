# BomBot

- Term Project for 15-112 (F21) at CMU
- BomBot Designed with PyGame

![Preview](./asset/image/preview.png)

## Sprites

**Robot**

- controlled by the user
- move in four directions: left, up, right, down
- place bomb

**Enemy**

- behave similar to Robot but try to kill robot

**Brick**

- destructible by Explosion

**Wall**

- non-destructible by Explosion

**Wall**

- once detonated, create Explosion

**Explosion**

- vertical and horizontal
- kill Robot and Enemy
- does not penetrate through Brick or Wall



## Controls

Below is a list containing all controls used in BomBot.

**Position**

- Move Robot: Arrows

**Bomb**

- Drop Bomb: Space



## Game AI

**Shortest-Path Finding**

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

**Check Safety**

- if in dangerous mode:
  - move to somewhere safe
  - stay in that place until bomb is detonated

**Bomb Robot**

- find the shortest path to Robot
- bomb Brick along the path
- reach Robot and BomBot



## Known Issues

**Board Generation**

  - by chance, large amount of emptiness in one location
  - by chance, robot is directly connected to other enemies without bombing bricks
  - by chance, large amount of bricks in one location
  - by chance, useless wall created (robot cannot enter space in between walls for shelter)

**Game AI**

- if a bomb is placed at where the Enemy is located, Enemy stuck there
- Enemy cannot perform random movements around the place

**Bomb**

- Sometimes, numBomb doesn't reload



### Citation

**Image**:

- Robot
  - I have used the  image below and modified its properties
  - https://appadvice.com/app/tiny-robot-stickers/1478530434
- Bomb
  - I have used the  image below and modified its properties
  - https://www.amazon.com/Bomb-Sounds-Sound-Effects-Atomic/dp/B07L37MGMV
- Wall
  - I have used the  image from this source and modified its properties
  - https://opengameart.org/content/dungeon-crawl-32x32-tiles
- Floor
  - I have used the  image from this source and modified its properties
  - https://opengameart.org/content/dungeon-crawl-32x32-tiles
- Brick
  - I have used the  image below and modified its properties
  - https://www.pinterest.com/pin/427701295834480905/
- Shoe
  - I have used the  image below and modified its properties
  - https://www.pinterest.co.uk/pin/258394097341915515/
- Potion
  - I have used the  image below and modified its properties
  - https://www.pinterest.co.uk/pin/258394097341915515/
- Lightening
  - I have used the  image below and modified its properties
  - https://www.pinterest.co.uk/pin/258394097341915515/

**Algorithm**:

- Dijkstra's Algorithm:
  - I have used the video below to understand how Dijkstra's Algorithm works
  - https://www.youtube.com/watch?v=pVfj6mxhdMw

**Code Snippet:**

- Not-Destructively Retrieve Element from a Set
  - I have incorporated code snippet from the following answer into BomBot
  - https://stackoverflow.com/a/59841/17254508
- Create Menu in Pygame
  - I have incorporated code snippet from the following tutorial into BomBot 
  - https://www.sourcecodester.com/tutorials/python/11784/python-pygame-simple-main-menu-selection.html

