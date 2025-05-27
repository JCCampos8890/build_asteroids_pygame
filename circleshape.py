import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class CircleShape(pygame.sprite.Sprite):
    """
    Base class for circular game objects with position, velocity,
    radius-based collisions, and screen wrapping.

    Subclasses should override draw() and update(dt) methods.
    """

    def __init__(self, x, y, radius):
        """
        Initialize a circular object with position and radius.

        Args:
            x (float): Initial X position.
            y (float): Initial Y position.
            radius (float): Collision radius.
        """
        # Add to sprite group if containers are defined in subclass
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        """
        Draw the object to the screen.
        Must be overridden by subclasses.
        """
        pass

    def update(self, dt):
        """
        Update the object's state.
        Must be overridden by subclasses.
        """
        pass

    def collide(self, other):
        """
        Check collision with another object (circle or rectangle).

        Args:
            other: Another object (with .position & .radius or .get_rect())

        Returns:
            bool: True if a collision is detected.
        """
        if hasattr(other, "get_rect"):
            # Circle vs Rectangle (e.g., shot vs boss)
            rect = other.get_rect()
            closest_x = max(rect.left, min(self.position.x, rect.right))
            closest_y = max(rect.top, min(self.position.y, rect.bottom))
            closest_point = pygame.Vector2(closest_x, closest_y)
            distance = self.position.distance_to(closest_point)
            return distance < self.radius

        elif hasattr(other, "position") and hasattr(other, "radius"):
            # Circle vs Circle
            distance = self.position.distance_to(other.position)
            return distance < (self.radius + other.radius)

        return False

    def wrap_position(self):
        """
        Wrap the object to the opposite screen edge if it exits the view.
        """
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
