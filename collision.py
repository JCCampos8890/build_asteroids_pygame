"""
Collision detection utilities for the space shooter game.

Supports:
- Circle vs Circle
- Circle vs Rect
- Rect vs Rect
- Automatic type-based detection via detect_collision()
"""

import pygame

def circle_vs_circle(circle1, circle2):
    """
    Detect collision between two circular objects.

    Args:
        circle1: Object with position (Vector2) and radius.
        circle2: Same as circle1.

    Returns:
        bool: True if circles overlap.
    """
    distance = circle1.position.distance_to(circle2.position)
    return distance < (circle1.radius + circle2.radius)

def circle_vs_rect(circle, rect):
    """
    Detect collision between a circle and a rectangle.

    Args:
        circle: Object with position (Vector2) and radius.
        rect: pygame.Rect to check against.

    Returns:
        bool: True if the circle overlaps the rect.
    """
    closest_x = max(rect.left, min(circle.position.x, rect.right))
    closest_y = max(rect.top, min(circle.position.y, rect.bottom))
    closest_point = pygame.Vector2(closest_x, closest_y)
    distance = circle.position.distance_to(closest_point)
    return distance < circle.radius

def rect_vs_rect(rect1, rect2):
    """
    Detect collision between two rectangles.

    Args:
        rect1: pygame.Rect
        rect2: pygame.Rect

    Returns:
        bool: True if rectangles overlap.
    """
    return rect1.colliderect(rect2)

def detect_collision(a, b):
    """
    Automatically detect collision type based on object properties.

    Supports:
        - Circle vs Circle (radius + radius)
        - Circle vs Rect (circle has .radius, other has .get_rect())
        - Rect vs Rect (both have .get_rect())

    Args:
        a, b: Any two game objects.

    Returns:
        bool: True if the objects collide.
    """
    if hasattr(a, "radius") and hasattr(b, "radius"):
        return circle_vs_circle(a, b)
    elif hasattr(a, "radius") and hasattr(b, "get_rect"):
        return circle_vs_rect(a, b.get_rect())
    elif hasattr(b, "radius") and hasattr(a, "get_rect"):
        return circle_vs_rect(b, a.get_rect())
    elif hasattr(a, "get_rect") and hasattr(b, "get_rect"):
        return rect_vs_rect(a.get_rect(), b.get_rect())

    return False
