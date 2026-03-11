# Python Games

A collection of four games built from scratch with Python and Pygame, each demonstrating progressively more advanced game development techniques -- from basic collision handling to tile-based maps, camera systems, and enemy AI.

---

## Games

### Pong

A faithful recreation of the classic arcade game featuring a human-controlled paddle against an AI opponent.

**Gameplay:**
Player vs. AI paddle game. Score points by getting the ball past the opponent. Scores persist between sessions via a JSON save file.

**Key Technical Features:**
- Frame-rate independent movement using delta time
- Per-axis collision detection to prevent ball tunneling
- AI opponent that tracks ball position with speed constraints
- Custom sprite group rendering with shadow effects
- Persistent scoring saved to disk

**Controls:** Arrow keys (Up / Down)

---

### Space Shooter

A top-down survival shooter with procedurally spawned meteors, projectile combat, and animated explosions.

**Gameplay:**
Pilot a ship, dodge falling meteors, and destroy them with lasers. Score is based on survival time. Meteors spawn at increasing frequency from random screen positions.

**Key Technical Features:**
- 21-frame explosion sprite animation with interpolated frame timing
- Continuous meteor rotation via `rotozoom` with cached original surfaces to prevent quality loss
- Pixel-perfect collision detection using sprite masks
- Custom Pygame timer events for periodic enemy spawning
- Layered audio system (BGM, laser, explosion) with volume control

**Controls:** Arrow keys to move, Space to fire

---

### Platformer

A 2D side-scrolling platformer with tile-based level design, directional shooting, and multiple enemy types.

**Gameplay:**
Navigate a tile-based world loaded from a Tiled TMX map. Jump across platforms, avoid or shoot enemies (bees and worms), and explore the level. Enemies spawn dynamically from the map's entity layer.

**Key Technical Features:**
- TMX tile map loading via `pytmx` with separate decoration, collision, and entity layers
- Player-centered camera system with offset rendering
- Two distinct enemy behaviors:
  - **Bee:** Sine-wave vertical oscillation with timed spawning
  - **Worm:** Ground patrol with boundary detection and direction flipping
- Reusable `Timer` class with repeat, autostart, and callback support
- Death animation using mask-based sprite silhouettes
- Batch asset loading utilities for sprite folders and audio files

**Controls:** Arrow keys to move, Up to jump, Space to shoot

---

### Vampire Survivor

A roguelike survival game inspired by the Vampire Survivors genre, featuring mouse-aimed combat, wave-based enemy spawning, and top-down depth sorting.

**Gameplay:**
Move through a large tile-based map using keyboard input while aiming and firing with the mouse. Enemies (bats, blobs, skeletons) spawn from predefined map positions in waves and chase the player. Survive as long as possible.

**Key Technical Features:**
- Mouse-based aiming with `atan2` angle calculation and conditional sprite flipping
- Gun attached to player with dynamic rotation and fire-position offset
- Top-down Y-depth sorting for correct visual layering of ground and object sprites
- Enemy AI with normalized direction vectors for smooth chase behavior
- Separate hitbox and render rects for precise collision handling
- Recursive folder traversal for dynamic loading of multi-type enemy animations
- TMX-based spawn point system for enemy wave generation

**Controls:** WASD to move, Mouse to aim, Left Click to shoot

---

## Project Structure

```
Python-Games/
|-- Pong/
|   |-- code/          # Game logic (main, ball, paddle, groups, settings)
|   |-- data/          # Persistent score file
|
|-- Space Shooter/
|   |-- code/          # Single-file game implementation
|   |-- images/        # Player, meteor, laser, and explosion sprites
|   |-- audio/         # Background music and sound effects
|
|-- Platform/
|   |-- code/          # Modular codebase (main, sprites, groups, support, timer, settings)
|   |-- data/          # TMX maps, tilesets, and graphics
|   |-- images/        # Player, enemy, and weapon sprites
|   |-- audio/         # Background music and sound effects
|
|-- Vampire survivor/
|   |-- code/          # Modular codebase (main, player, sprites, groups, settings)
|   |-- data/          # TMX maps, tilesets, and graphics
|   |-- images/        # Player, enemy, and weapon sprites
|   |-- audio/         # Background music and sound effects
```

---

## Requirements

- Python 3.10+
- Pygame
- pytmx (for Platformer and Vampire Survivor)
