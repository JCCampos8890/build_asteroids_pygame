# 🚀 AngryAsteroids: Pygame Space Adventure

A hilarious and chaotic take on the classic *Asteroids* game 
— now starring a custom spaceship (my girlfriend!) and asteroids (myself). Built with Python + Pygame and packed with sounds, visuals, and endless fun!

---

## 🎮 Gameplay Highlights

- **Custom images**: Your spaceship and asteroids are literally ME (and my girlfriend 😎)
- **Smooth controls**: Rotate, thrust, and shoot with intuitive keyboard input
- **Realistic movement**: Velocity, friction, momentum, and wrapping space
- **Asteroid splitting**: Larger asteroids split into smaller ones when hit
- **Lives system**: Lose lives on impact — with temporary invincibility and visual feedback
- **Dynamic difficulty**: Game scales in intensity as you level up
- **Score tracking & levels** (coming soon!)
- **Boss battles** (coming soon!)

---

## 🎧 Custom Sound Effects

- Shooting, collisions, and game over events have real audio clips recorded by the dev
- Balanced volumes and cooldowns prevent sound chaos

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| ← / → | Rotate ship |
| ↑ | Thrust forward |
| Spacebar | Shoot |
| ESC | Quit game |

---

## 🧠 How It Works

- Modular code structure (`player.py`, `asteroid.py`, `shot.py`, etc.)
- Sprite groups for update and draw logic
- Timer-based level progression
- Wrapping logic keeps everything looping around the screen
- Asteroids now vanish after 3 wraps to avoid long chases

---

## 🖼️ Assets

- Custom PNG images with transparent backgrounds
- Flame animation when thrusting
- Pixel-perfect collision detection using circles

---

## 📦 Getting Started

1. Clone the repo  
   ```bash
   [git clone https://github.com/JCCampos8890/build_asteroids_pygame)
   cd AngryAsteroids
