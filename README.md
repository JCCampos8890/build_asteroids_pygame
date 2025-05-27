# 🚀 AngryLove & Asteroids: A Pygame Space Adventure

A chaotic, hilarious, and hand-crafted take on the classic *Asteroids* arcade game — starring my girlfriend as the pilot, me as the asteroids, and my dog as the final boss. Built with Python + Pygame as a portfolio passion project.

![Gameplay GIF](assets/demo.gif) <!-- Replace with actual GIF path -->

---

## 🚮 Why I Built This

This project began as a fun way to learn Pygame, but quickly evolved into a full-featured game with custom enemies, levels, and cutscenes. I wanted to:

* Build something original and funny with people I love
* Practice clean, modular game architecture in Python
* Create polished features from sound, UI, and collision systems

This game helped sharpen my logic, animation, and debugging skills. And it made my friends laugh. Win-win.

---

## 🎓 What I Learned

* Object-Oriented Game Architecture
* Sprite Group Management in Pygame
* Circle and Rectangle Collision Detection
* Frame-based Animation and State Machines
* Sound Integration and Custom Debugging Tools

---

## 🎮 Gameplay Features

* 🚗 **Custom Ship**: My girlfriend flies the ship
* 🪨 **Asteroids Are Me**: Literally my face on space rocks
* 🚶 **Mikitos**: Funny baby dog enemies that shoot poop to make you dizzy
* 🐶 **Final Boss Mika**: Two epic stages with cookie bombs and mikitos spawns
* 🔄 Wrapping screen edges like a true space sim
* ✨ Visual feedback when hit (flashing, dizzy, invincible)
* 🎧 Real sound effects recorded by me (yes, including "iugh.wav")
* 🏆 Victory cutscene and boss defeat sequence

---

## 🔧 Tech Stack

* Python 3.11+
* Pygame 2.x
* OOP-based modular design
* SpriteGroups for update/draw
* Custom collision & movement logic

---

## ⌨️ Controls

| Key   | Action              |
| ----- | ------------------- |
| ← / → | Rotate spaceship    |
| ↑     | Thrust forward      |
| Space | Shoot               |
| R     | Restart (Game Over) |
| Q     | Quit (Game Over)    |

---

## 🔮 Developer Mode

Enable extra features in `devtools.py`:

```python
DEV_MODE = True        # Start at any level instantly
SKIP_TO_LEVEL = 10     # Skip to boss for testing
GOD_MODE = True        # Infinite lives
SHOW_HITBOXES = True   # Show all entity hitboxes
```

---

## 📂 Project Structure

```
.
├── main.py             # Game loop & state manager
├── asteroid.py         # Asteroid logic and splitting
├── enemy.py            # Mikito AI and bullets
├── finalboss.py        # Mika boss phases and cookies
├── player.py           # Movement, shooting, dizzy logic
├── shot.py             # Projectiles
├── screens.py          # Intro, game over, cutscenes
├── circleshape.py      # Base class for circular sprites
├── rectangleshape.py   # Base class for boss hitboxes
├── constants.py        # All tunable values
├── devtools.py         # Debug toggles and cheats
└── assets/             # Images, sounds, and fonts
```

---

## 📊 Getting Started

1. **Clone the repo**

```bash
git clone https://github.com/JCCampos8890/build_asteroids_pygame
cd build_asteroids_pygame
```

2. **Install dependencies**

```bash
pip install pygame
```

3. **Launch the game**

```bash
python main.py
```

---

## 💍 Credits

Created by [@JCCampos8890](https://github.com/JCCampos8890)

Special thanks to:

* My girlfriend (for being the pilot and recording the sounds)
* My dog Mika (for being the most awesome boss)
* Pygame + OpenGameArt


