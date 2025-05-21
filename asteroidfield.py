import pygame
import random
from asteroid import Asteroid, TIERS
from constants import *

# AsteroidField class that manages the spawning and updating of asteroids
class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, asteroid_group):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.asteroid_group = asteroid_group
        self.spawn_timer = 0.0
        self.elapsed_time = 0.0
        self.level = 1

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        print(f"Spawning asteroid | Radius: {radius:.1f} | Pos: {position} | Speed: {velocity.length():.1f}")

    def update(self, dt):
        self.spawn_timer += dt
        self.elapsed_time += dt

        # Level up every 15 seconds
        if self.elapsed_time > self.level * 15:
            self.level += 1
            print(f"\U0001F680 Level up! Now at level {self.level}")

        # Gradual difficulty scaling
        spawn_rate = max(ASTEROID_SPAWN_RATE - (self.level * 0.02), 0.6)

        if self.spawn_timer > spawn_rate:
            self.spawn_timer = 0

            max_asteroids = min(3 + self.level, 10)
            if len(self.asteroid_group) >= max_asteroids:
                return  # Avoid overcrowding

            edge = random.choice(self.edges)
            position = edge[1](random.uniform(0, 1))

            min_speed = 40 + (self.level * 2)
            max_speed = 80 + (self.level * 4)
            speed = random.randint(min_speed, max_speed)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))

            # Spawn only big asteroids initially, split will create smaller
            if self.level < 3:
                radius = 50
            elif self.level < 5:
                radius = random.choice([50, 20])
            else:
                radius = random.choice([50, 20, 10])

            self.spawn(radius, position, velocity)
