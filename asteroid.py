"""
Defines the Asteroid class for destructible, rotating, and splitting space rocks.

- Asteroids spawn in different tiers (sizes).
- When destroyed, large asteroids split into smaller ones.
- Each asteroid rotates, moves, and wraps around the screen.
- Includes optional debug hitbox rendering via SHOW_HITBOXES.
"""

import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from devtools import SHOW_HITBOXES

# --- Asteroid Tier System ---
TIERS = [50, 20, 10]  # Large, Medium, Small


class Asteroid(CircleShape):
    """
    Asteroid object with rotation, wrapping, and splitting behavior.

    Inherits from CircleShape for position, velocity, and screen logic.
    """

    def __init__(self, x, y, base_radius):
        """
        Initialize an asteroid of a given tier.

        Args:
            x (float): Starting X position.
            y (float): Starting Y position.
            base_radius (int): Size tier (must be in TIERS).
        """
        self.base_radius = base_radius
        self.wrap_count = 0  # Track how many times the asteroid wraps around the screen

        # Load and scale the asteroid image
        original_image = pygame.image.load("assets/asteroid.png").convert_alpha()
        visual_scale = 3.5
        diameter = base_radius * visual_scale
        self.image = pygame.transform.scale(original_image, (int(diameter), int(diameter)))

        # Set hitbox radius to half the final image size (for a perfect visual match)
        self.radius = self.image.get_width() // 2.2

        # Initialize physics and position
        super().__init__(x, y, self.radius)

        # Random rotation speed (in degrees per second)
        self.rotation = 0
        self.rotation_speed = random.uniform(-90, 90)

    def draw(self, screen):
        """
        Draw the asteroid with its current rotation and optional hitbox.

        Args:
            screen (Surface): The Pygame screen surface to draw on.
        """
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_image, rect)

        if SHOW_HITBOXES:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (int(self.position.x), int(self.position.y)),
                int(self.radius),
                1
            )

    def update(self, dt):
        """
        Update the asteroid's position, rotation, and screen wrapping.

        Asteroids disappear after wrapping 3 times.

        Args:
            dt (float): Time delta in seconds.
        """
        self.rotation += self.rotation_speed * dt
        self.position += self.velocity * dt

        old_position = self.position.copy()
        self.wrap_position()

        # Count screen wraps and destroy after 3
        if old_position.x != self.position.x or old_position.y != self.position.y:
            self.wrap_count += 1
            if self.wrap_count >= 3:
                self.kill()

    def split(self):
        """
        Split this asteroid into two smaller ones if it can.

        Large splits into medium, medium into small, small disappears.
        """
        self.kill()

        # Only split if the size is in TIERS
        if self.base_radius not in TIERS:
            return

        current_index = TIERS.index(self.base_radius)

        # Already the smallest? No split
        if current_index + 1 >= len(TIERS):
            return

        new_radius = TIERS[current_index + 1]

        # Create two new asteroids at a small angle difference
        angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(angle) * 1.2
        v2 = self.velocity.rotate(-angle) * 1.2
        x, y = self.position.x, self.position.y

        Asteroid(x, y, new_radius).velocity = v1
        Asteroid(x, y, new_radius).velocity = v2
