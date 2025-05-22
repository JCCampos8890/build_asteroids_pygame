import pygame
import random
from asteroid import Asteroid, TIERS
from constants import *
from enemy import Enemy

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self, asteroid_group, enemy_group, player, bullet_group):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.asteroid_group = asteroid_group
        self.enemy_group = enemy_group
        self.player = player
        self.bullet_group = bullet_group

        self.spawn_timer = 0.0
        self.enemy_spawn_timer = 0.0  
        self.elapsed_time = 0.0
        self.level = 1
        self.max_enemies = 3  # Mikitos


    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        print(f"Spawning asteroid | Radius: {radius:.1f} | Pos: {position} | Speed: {velocity.length():.1f}")

    def update(self, dt):
        self.spawn_timer += dt
        self.elapsed_time += dt
        self.enemy_spawn_timer += dt

        if self.elapsed_time > self.level * 15:
            self.level += 1
            print(f"🚀 Level up! Now at level {self.level}")

        spawn_rate = max((ASTEROID_SPAWN_RATE - (self.level * 0.02)) * 1.43, 0.6)

        if self.spawn_timer > spawn_rate:
            self.spawn_timer = 0

            max_asteroids = min(3 + self.level, 10)
            if len(self.asteroid_group) >= max_asteroids:
                return

            edge = random.choice(self.edges)
            position = edge[1](random.uniform(0, 1))

            min_speed = 40 + (self.level * 2)
            max_speed = 80 + (self.level * 4)
            speed = random.randint(min_speed, max_speed)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))

            if self.level < 3:
                radius = 50
            elif self.level < 5:
                radius = random.choice([50, 20])
            else:
                radius = random.choice([50, 20, 10])

            self.spawn(radius, position, velocity)

        # Mikito enemy spawn logic
        if self.level >= 5 and self.enemy_spawn_timer > 6.0:
            self.enemy_spawn_timer = 0

            if len(self.enemy_group) < self.max_enemies:
                x = random.choice([-40, SCREEN_WIDTH + 40])
                y = random.uniform(50, SCREEN_HEIGHT - 50)
                Enemy(x, y, self.player, self.bullet_group)

