"""
Developer tool flags for testing and debugging the game.

These constants allow you to modify gameplay behavior without
changing the game logic directly.
"""

# --- Core Dev Mode Switch ---

DEV_MODE = True       # Set to False for normal gameplay

# --- Testing Shortcuts ---

SKIP_TO_LEVEL = 10     # Start game at a specific level (e.g., skip to boss fight)
GOD_MODE = False       # Player doesn't lose lives
FAST_RESPAWN = False   # Speeds up cooldowns or enemy spawns (optional)

# --- Visual Debugging ---

SHOW_HITBOXES = False  # Show hitboxes for all entities (if implemented)
