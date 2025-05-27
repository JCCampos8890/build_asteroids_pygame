import pygame
import random
from asteroid import Asteroid, TIERS
from constants import *
from enemy import Enemy

class AsteroidField(pygame.sprite.Sprite):
    """
    Manages spawning of asteroids and Mikito enemies based on the game level.

    Asteroids spawn from screen edges with increasing frequency and speed.
    Mikitos begin appearing from level 5 onward.
    """

    # Edge definitions for asteroid spawning (direction vector, position generator)
    edges = [
        [pygame.Vector2(1, 0),   lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],  # Left
        [pygame.Vector2(-1, 0),  lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],  # Right
        [pygame.Vector2(0, 1),   lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS)],  # Top
        [pygame.Vector2(0, -1),  lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS)],  # Bottom
    ]

    def __init__(self, asteroid_group, enemy_group, player, bullet_group):
        """
        Initialize the asteroid field system.

        Args:
            asteroid_group (Group): Pygame group for asteroids.
            enemy_group (Group): Pygame group for Mikito enemies.
            player (Player): Player reference for spawn distance checks.
            bullet_group (Group): Group to assign new Mikito bullets to.
        """
        super().__init__(self.containers)
        self.asteroid_group = asteroid_group
        self.enemy_group = enemy_group
        self.player = player
        self.bullet_group = bullet_group

        self.spawn_timer = 0.0
        self.enemy_spawn_timer = 0.0
        self.elapsed_time = 0.0
        self.level = 1
        self.max_enemies = 3  # Limit on concurrent Mikitos

    def spawn(self, radius, position, velocity):
        """
        Spawn a new asteroid unless it's too close to the player.

        Args:
            radius (int): Size of asteroid (from TIERS).
            position (Vector2): Spawn location.
            velocity (Vector2): Initial movement vector.
        """
        safe_distance = 150  # Avoid spawning too close to player
        if self.player.position.distance_to(position) < safe_distance:
            return  # Skip spawning

        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        print(f"Spawning asteroid | Radius: {radius:.1f} | Pos: {position} | Speed: {velocity.length():.1f}")

    def update(self, dt):
        """
        Called each frame to potentially spawn new asteroids and enemies.

        Args:
            dt (float): Delta time in seconds.
        """
        self.spawn_timer += dt
        self.enemy_spawn_timer += dt
        self.elapsed_time += dt

        # Level progression based on time survived
        if self.elapsed_time > self.level * 15:
            self.level += 1
            print(f"🚀 Level up! Now at level {self.level}")

        # --- Asteroid Spawning ---

        # Dynamic spawn rate (faster as level increases)
        spawn_rate = max((ASTEROID_SPAWN_RATE - (self.level * 0.02)) * 1.43, 0.6)

        if self.spawn_timer > spawn_rate:
            self.spawn_timer = 0

            max_asteroids = min(3 + self.level, 10)
            if len(self.asteroid_group) >= max_asteroids:
                return  # Skip if too many asteroids already

            # Choose a random edge to spawn from
            edge = random.choice(self.edges)
            position = edge[1](random.uniform(0, 1))

            # Speed increases per level
            min_speed = 40 + (self.level * 2)
            max_speed = 80 + (self.level * 4)
            speed = random.randint(min_speed, max_speed)

            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))

            # Choose asteroid size based on level
            if self.level < 3:
                radius = 50
            elif self.level < 5:
                radius = random.choice([50, 20])
            else:
                radius = random.choice([50, 20, 10])

            self.spawn(radius, position, velocity)

        # --- Enemy Spawning (Mikitos) ---

        if self.level >= 5 and self.enemy_spawn_timer > 6.0:
            self.enemy_spawn_timer = 0

            if len(self.enemy_group) < self.max_enemies:
                # Spawn Mikito from left or right
                x = random.choice([-40, SCREEN_WIDTH + 40])
                y = random.uniform(50, SCREEN_HEIGHT - 50)

                enemy = Enemy(
                    x=x,
                    y=y,
                    player=self.player,
                    bullet_group=self.bullet_group,
                    dizzy_only=True  # Mikitos use dizzy effect, not damage
                )

                self.enemy_group.add(enemy)
