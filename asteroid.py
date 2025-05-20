
import pygame
from circleshape import CircleShape
import random
from constants import ASTEROID_MIN_RADIUS

# Asteroid class that represents the asteroids in the game
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0  # Track current rotation angle
        self.rotation_speed = random.uniform(-90, 90)  # degrees per second

    # Draws the asteroid on the screen
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, width=2)

    # Updates the asteroid position and rotation
    def update(self, dt):
        self.rotation += self.rotation_speed * dt
        self.position += self.velocity * dt

    # Splits the asteroid into two smaller asteroids
    def split(self):
        self.kill()  # destroy the current asteroid
     
        if self.radius <= ASTEROID_MIN_RADIUS:           # If it's too small to split, just disappear
            return
        
        random_angle = random.uniform(20, 50)            # Generate a random split angle
        
        # Rotate velocity in two opposite directions
        velocity1 = self.velocity.rotate(random_angle) * 1.2
        velocity2 = self.velocity.rotate(-random_angle) * 1.2

        new_radius = self.radius - ASTEROID_MIN_RADIUS    # Calculate new radius (shrink by 1 level)

        # Spawn two new asteroids at the same position
        x, y = self.position.x, self.position.y
        Asteroid(x, y, new_radius).velocity = velocity1
        Asteroid(x, y, new_radius).velocity = velocity2
