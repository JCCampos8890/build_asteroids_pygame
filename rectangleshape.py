"""
RectangleShape base class for rectangular game objects.

- Used for enemies or bosses with rectangular bounds (currently just used for the boss).
- Includes support for screen wrapping and collision detection with circles or rects.
"""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class RectangleShape(pygame.sprite.Sprite):
    """
    Base class for rectangular entities in the game.

    Provides position, size, velocity, screen wrapping,
    and collision detection (rect-rect and circle-rect).
    """

    def __init__(self, x, y, width, height):
        """
        Initialize a rectangle-shaped sprite.

        Args:
            x (float): Center X position.
            y (float): Center Y position.
            width (int): Width of the rectangle.
            height (int): Height of the rectangle.
        """
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.velocity = pygame.Vector2(0, 0)

    @property
    def rect(self):
        """
        pygame.Rect aligned to self.position as center.

        Returns:
            pygame.Rect: Rectangle representing the object's bounds.
        """
        return pygame.Rect(
            int(self.position.x - self.width // 2),
            int(self.position.y - self.height // 2),
            self.width,
            self.height
        )

    def get_rect(self):
        """
        Returns the current bounding rectangle (alias of self.rect).

        Returns:
            pygame.Rect: Current bounding rectangle.
        """
        return self.rect

    def draw(self, screen):
        """
        Subclasses should override to render the object.
        """
        pass

    def update(self, dt):
        """
        Subclasses should override to update object logic.

        Args:
            dt (float): Delta time in seconds.
        """
        pass

    def collide(self, other):
        """
        Detect collision with another object.

        Supports:
            - Rect vs Rect (if other has .get_rect())
            - Circle vs Rect (if other has .position and .radius)

        Args:
            other: Another game object.

        Returns:
            bool: True if objects collide.
        """
        if hasattr(other, "get_rect"):
            return self.rect.colliderect(other.get_rect())

        elif hasattr(other, "position") and hasattr(other, "radius"):
            # Circle vs Rectangle
            rect = self.get_rect()
            closest_x = max(rect.left, min(other.position.x, rect.right))
            closest_y = max(rect.top, min(other.position.y, rect.bottom))
            closest_point = pygame.Vector2(closest_x, closest_y)
            return other.position.distance_to(closest_point) < other.radius

        return False

    def wrap_position(self):
        """
        Wrap the object to the opposite screen edge if it exits the screen.
        """
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
