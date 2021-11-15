# BomBot

- Term Project for 15-112 (F21) at CMU
- BomBot Designed with PyGame

![Preview](./asset/image/preview.png)

## Entities

Below is a list containing all entities used in BomBot.

### Board

- stores position of everything fixed
- "w" for wall, "p" for player, "f" for floor

### Robot

- determined by (x, y)
- is controlled by the user

### Brick

- determined by (r, c)
- destructible

### Wall

- determined by (r, c)

- non-destructible

### Floor

- determined by (r, c)

- where everything sits on

### Enemy

- behaves like a user

### Bomb

- determined by (r, c)

- once placed, 3 seconds to detonation
- destructs brick and kills enemy
- explosion is vertical and horizontal

### Explosion

- determined by (r, c)
- triggered by bomb

## Controls

Below is a list containing all controls used in BomBot.

### Position

- Move Left: Left-Arrow
- Move Up: Up-Arrow
- Move Right: Right-Arrow
- Move Down: Down-Arrow

### Bomb

- Drop Bomb: Space



