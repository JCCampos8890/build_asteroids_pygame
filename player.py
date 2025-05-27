"""
Player class.

Features:
- Movement with rotation and thrust.
- Shooting bullets with cooldown.
- Dizzy status effect (inverts controls and wobbles visuals).
- Invincibility timer after losing a life.
- Screen wrapping or bounded edge handling.
"""

import pygame
import math
from constants import *
from circleshape import CircleShape
from shot import Shot
from devtools import SHOW_HITBOXES

class Player(CircleShape):
    """
    The player's spaceship: handles input, movement, shooting,
    status effects, and visual state.
    """

    def __init__(self, x, y, shoot_sound):
        """
        Initialize the player with position and ship assets.

        Args:
            x (float): Initial X position.
            y (float): Initial Y position.
            shoot_sound (Sound): Sound to play when firing.
        """
        diameter = PLAYER_RADIUS * 4
        self.ship_img = pygame.transform.scale(
            pygame.image.load("assets/ship.png").convert_alpha(), (diameter, diameter)
        )
        self.ship_flame_img = pygame.transform.scale(
            pygame.image.load("assets/shipflame.png").convert_alpha(), (diameter, diameter)
        )
        self.ship_flame_img_dizzy = pygame.transform.scale(
            pygame.image.load("assets/shipflame_dizzy.png").convert_alpha(), (diameter, diameter)
        )

        self.image = self.ship_img
        self.ship_img_red = self._tint_image(self.ship_img, (255, 80, 80))
        self.ship_flame_img_red = self._tint_image(self.ship_flame_img, (255, 80, 80))

        visual_radius = diameter // 2.1
        super().__init__(x, y, visual_radius)

        # Movement & physics
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 200
        self.friction = 0.98
        self.max_speed = 400
        self.timer = 0.0

        # Player state
        self.lives = 5
        self.invincible = False
        self.invincibility_timer = 0.0
        self.dizzy = False
        self.dizzy_timer = 0.0
        self.disable_wrap = False

        self.shoot_sound = shoot_sound

    def collide(self, other):
        """
        Check collision with another object.

        Supports:
        - Circle vs Rectangle (boss)
        - Circle vs Circle (asteroid, enemy)

        Args:
            other: Object with either get_rect() or position + radius.

        Returns:
            bool: True if a collision occurred.
        """
        if hasattr(other, 'get_rect') and callable(other.get_rect):
            rect = other.get_rect()
            closest_x = max(rect.left, min(self.position.x, rect.right))
            closest_y = max(rect.top, min(self.position.y, rect.bottom))
            distance = self.position.distance_to((closest_x, closest_y))
            return distance < self.radius

        elif hasattr(other, 'position') and hasattr(other, 'radius'):
            return self.position.distance_to(other.position) < (self.radius + other.radius)

        return False

    def _tint_image(self, image, tint_color):
        """
        Apply a color tint overlay to an image for flashing effects when losing lives.
        """
        tinted = image.copy()
        tint_surface = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        tint_surface.fill(tint_color + (0,))
        tinted.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted

    def draw(self, screen):
        """
        Draw the player ship with rotation, flame, dizzy effects, and optional hitbox.
        """
        if self.image in (self.ship_flame_img, self.ship_flame_img_dizzy):
            base_image = self.ship_flame_img_dizzy if self.dizzy else self.ship_flame_img
            red_image = self._tint_image(base_image, (255, 80, 80))
        else:
            base_image = self.ship_img
            red_image = self.ship_img_red

        image_to_draw = red_image if self.invincible and (pygame.time.get_ticks() // 100) % 2 == 0 else base_image

        wobble_offset = 5 * math.sin(pygame.time.get_ticks() / 100) if self.dizzy else 0
        rotated_image = pygame.transform.rotate(image_to_draw, -self.rotation + wobble_offset)
        rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_image, rect)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, (0, 255, 255), (int(self.position.x), int(self.position.y)), int(self.radius), 1)

    def rotate(self, dt):
        """
        Rotate the ship to the right.
        """
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        """
        Update player position, input, status effects, and shooting.

        Args:
            dt (float): Delta time in seconds.
        """
        keys = pygame.key.get_pressed()

        # --- Dizzy timer countdown ---
        if self.dizzy:
            self.dizzy_timer -= dt
            if self.dizzy_timer <= 0:
                self.dizzy = False

        # --- Input handling (inverted if dizzy) ---
        left, right, up = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP
        if self.dizzy:
            left, right = right, left

        if keys[left]:
            self.rotate(-dt)
        if keys[right]:
            self.rotate(dt)

        if keys[up]:
            thrust = pygame.Vector2(0, -1).rotate(self.rotation)
            self.velocity += thrust * self.acceleration * dt

        # --- Image selection for flame effect ---
        self.image = (
            self.ship_flame_img_dizzy if self.dizzy else
            self.ship_flame_img if keys[up] else
            self.ship_img
        )

        # --- Movement & physics ---
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * dt
        self.velocity *= self.friction

        # --- Shooting ---
        self.timer -= dt
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()
            self.timer = PLAYER_SHOOT_COOLDOWN

        # --- Invincibility countdown ---
        if self.invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False

        # --- Screen bounds ---
        if self.disable_wrap:
            self.enforce_screen_bounds()
        else:
            self.wrap_position()

    def enforce_screen_bounds(self):
        """
        Prevent player from leaving screen during boss fight.
        """
        buffer = self.radius * 0.8

        if self.position.x < buffer:
            self.position.x = buffer
            self.velocity.x = 0
        elif self.position.x > SCREEN_WIDTH - buffer:
            self.position.x = SCREEN_WIDTH - buffer
            self.velocity.x = 0

        if self.position.y < buffer:
            self.position.y = buffer
            self.velocity.y = 0
        elif self.position.y > SCREEN_HEIGHT - buffer:
            self.position.y = SCREEN_HEIGHT - buffer
            self.velocity.y = 0

    def shoot(self):
        """
        Fire a projectile in the direction the player is facing.
        """
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        spawn_position = self.position + forward * self.radius
        Shot(spawn_position.x, spawn_position.y, velocity)
        self.shoot_sound.play()

    def lose_life(self):
        """
        Handle life loss. Trigger invincibility or end game if lives reach 0.

        Returns:
            bool: True if no lives remain (game over).
        """
        self.lives -= 1
        self.dizzy = False
        self.dizzy_timer = 0

        if self.lives <= 0:
            return True
        else:
            self.invincible = True
            self.invincibility_timer = 2.0
            return False

    def apply_dizzy(self, duration=3.0):
        """
        Apply dizzy status effect (inverted controls + wobble).

        Args:
            duration (float): Duration in seconds.
        """
        self.dizzy = True
        self.dizzy_timer = duration
        pygame.mixer.Sound("assets/iugh.wav").play()

    def push_back_from(self, source_position, force=8):
        """
        Push the player away from a given source (enemy, boss, etc).

        Args:
            source_position (Vector2): Origin of push.
            force (float): Pushback strength.
        """
        direction = self.position - source_position
        if direction.length() > 0:
            self.velocity += direction.normalize() * force
