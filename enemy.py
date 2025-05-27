"""
Enemy (Mikito) and EnemyBullet classes.

Mikito:
- Harmless enemy that chases the player and shoots dizzy-inducing poop bullets.
- Contact does not cause damage, only pushback.
- Projectiles only apply the 'dizzy' effect (inverted controls).

EnemyBullet:
- Non-lethal projectile with a dizzy status effect.
- Self-destructs if it moves too far off screen.
"""

import pygame
import random
import math
from circleshape import CircleShape
from constants import ENEMY_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from devtools import SHOW_HITBOXES

# --- Harmless enemy that shoots dizzy-inducing poop bullets ---

class Enemy(CircleShape):
    """
    Mikito enemy that follows the player and fires dizzy-inducing poop bullets.
    Contact with the player causes pushback, not damage.
    """

    def __init__(self, x, y, player, bullet_group, dizzy_only=True):
        """
        Initialize a Mikito enemy.

        Args:
            x (float): Initial X position.
            y (float): Initial Y position.
            player (Player): Reference to the player.
            bullet_group (Group): Group to store poop bullets.
            dizzy_only (bool): Always True for Mikito (bullets only cause dizzy effect).
        """
        image = pygame.image.load("assets/mikito.png").convert_alpha()
        diameter = ENEMY_RADIUS * 5.0
        self.image = pygame.transform.scale(image, (int(diameter), int(diameter)))

        super().__init__(x, y, diameter // 2.2)

        self.player = player
        self.bullet_group = bullet_group
        self.dizzy_only = dizzy_only

        self.speed = 40
        self.rotation = 0
        self.shoot_timer = random.uniform(3.0, 5.0)
        self.wobble_time = 0.0  # For animated wobble effect

    def update(self, dt):
        """
        Update Mikito's position, wobble animation, and shooting timer.

        Args:
            dt (float): Delta time in seconds.
        """
        # --- Follow the player ---
        if self.player:
            direction = self.player.position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * self.speed * dt

        # --- Wobble effect (side-to-side) ---
        self.wobble_time += dt
        self.rotation = 10 * math.sin(self.wobble_time * 4)

        # --- Shooting poop bullets ---
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = random.uniform(3.0, 5.0)

        self.wrap_position()

    def shoot(self):
        """
        Fire a dizzy poop bullet toward the player.
        """
        direction = self.player.position - self.position
        if direction.length() == 0:
            return

        direction = direction.normalize()
        bullet = EnemyBullet(
            self.position.x,
            self.position.y,
            direction * 120,
            is_dizzy=True  # Mikito bullets always cause dizziness
        )
        self.bullet_group.add(bullet)

    def draw(self, screen):
        """
        Draw the rotated Mikito and its hitbox if debugging is enabled.
        """
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_image, rect)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), int(self.radius), 1)


# --- Dizzy-inducing projectile (poop) shot by Mikito ---

class EnemyBullet(CircleShape):
    """
    Poop bullet that causes dizziness (inverted controls).
    Does not deal damage or cost lives.
    """

    def __init__(self, x, y, velocity, is_dizzy=True):
        """
        Initialize a dizzy-inducing projectile.

        Args:
            x (float): Initial X position.
            y (float): Initial Y position.
            velocity (Vector2): Movement vector.
            is_dizzy (bool): Always True for Mikito bullets.
        """
        super().__init__(x, y, 12)
        self.velocity = velocity
        self.is_dizzy = is_dizzy

        self.image = pygame.image.load("assets/mikitoshot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (24, 24))

    def update(self, dt):
        """
        Move the bullet and kill it if far off-screen.

        Args:
            dt (float): Delta time in seconds.
        """
        self.position += self.velocity * dt
        self.wrap_position()

        # Remove if too far outside screen bounds
        if (
            self.position.x < -50 or self.position.x > SCREEN_WIDTH + 50 or
            self.position.y < -50 or self.position.y > SCREEN_HEIGHT + 50
        ):
            self.kill()

    def draw(self, screen):
        """
        Draw the bullet and hitbox if enabled.
        """
        rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(self.image, rect)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), int(self.radius), 1)
