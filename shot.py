"""
Defines the Shot class used for player projectiles.
Simple circular bullets that travel in a straight line and wrap with the screen.
"""

import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS
from devtools import SHOW_HITBOXES


class Shot(CircleShape):
    """
    Projectile fired by the player.

    Inherits from CircleShape for position, radius, and basic wrapping behavior.
    """

    def __init__(self, x, y, velocity):
        """
        Initialize the shot with position and movement vector.

        Args:
            x (float): Initial X position.
            y (float): Initial Y position.
            velocity (Vector2): Direction and speed of the shot.
        """
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = velocity

    def draw(self, screen):
        """
        Render the shot as a white circle. Optional hitbox overlay.

        Args:
            screen: Surface to draw on.
        """
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), self.radius, 1)

    def update(self, dt):
        """
        Update the position of the shot based on its velocity.

        Args:
            dt (float): Delta time in seconds.
        """
        self.position += self.velocity * dt
