"""
Global constants for the 2D space shooter game.

Organized by category for easy maintenance and clarity.
"""

# --- Screen Settings ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# --- Asteroid Settings ---
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3  # Number of size tiers: large, medium, small
ASTEROID_SPAWN_RATE = 0.8  # Seconds between spawns
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # e.g., 60

# --- Player Settings ---
PLAYER_RADIUS = 30
PLAYER_TURN_SPEED = 300  # Degrees per second
PLAYER_SPEED = 200       # Pixels per second

# --- Player Shooting ---
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500             # Shot velocity
PLAYER_SHOOT_COOLDOWN = 0.3          # Time between shots (in seconds)

# --- Enemy Settings ---
ENEMY_RADIUS = 18  # For Mikito or other regular enemies

# --- Final Boss Settings ---
BOSS_HEALTH = 60
BOSS_STAGE1_HEALTH = 30
BOSS_STAGE2_HEALTH = 30

BOSS_RADIUS = 250                  # Half of the image size (500x500)
BOSS_SPEED_Y = 20                 # Vertical speed
BOSS_ENTRY_X = SCREEN_WIDTH - 200  # X position where boss enters the screen

# --- Boss Bullet Damage ---
BONE_DAMAGE = 10
COOKIE_DAMAGE = 20

# --- Boss Bullet Spawn Offsets ---
BONE_OFFSET_Y = 60
COOKIE_OFFSET_Y = -60
