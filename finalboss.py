"""
FinalBoss and its bullet classes.

- FinalBoss enters from the right and transitions into a second stage mid-fight.
- Stage 1: Moves vertically and fires bone bullets.
- Stage 2: Adds cookie bombs and Mikito spawns.
- Bullets include:
    - BoneBullet: fast rotating projectile.
    - CookieBullet: slow, larger projectile with health that can be destroyed.
"""

import pygame
import random
from circleshape import CircleShape
from rectangleshape import RectangleShape
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BOSS_HEALTH, BOSS_STAGE1_HEALTH, BOSS_STAGE2_HEALTH,
    BOSS_ENTRY_X, BOSS_SPEED_Y,
    BONE_DAMAGE, COOKIE_DAMAGE,
    BONE_OFFSET_Y, COOKIE_OFFSET_Y
)
from devtools import SHOW_HITBOXES
from enemy import Enemy

# --- Final Boss Class ---

class FinalBoss(RectangleShape):
    """
    The final boss that enters at level 10.

    Stage 1:
        - Moves vertically within bounds.
        - Fires bone bullets at regular intervals.

    Stage 2:
        - Switches to new sprite.
        - Moves faster.
        - Occasionally fires cookie bombs.
        - Periodically spawns Mikito enemies.
    """

    def __init__(self, player, mikito_group, bullet_group, mikito_bullets):
        """
        Initialize the boss and prepare stage data.

        Args:
            player (Player): Reference to the player.
            mikito_group (Group): Where new Mikitos are added.
            bullet_group (Group): Where boss bullets are added.
            mikito_bullets (Group): Passed to new Mikitos for poop bullets.
        """
        # Load and scale boss images
        self.image_stage1 = pygame.transform.scale(
            pygame.image.load("assets/boss_stage_1.png").convert_alpha(), (400, 500)
        )
        self.image_stage2 = pygame.transform.scale(
            pygame.image.load("assets/boss_stage_2.png").convert_alpha(), (400, 500)
        )
        self.image = self.image_stage1

        # Set up hitbox smaller than image
        raw_width, raw_height = self.image.get_size()
        width = int(raw_width * 0.7)
        height = int(raw_height * 0.7)
        x = SCREEN_WIDTH + width // 2
        y = SCREEN_HEIGHT // 2

        super().__init__(x, y, width, height)

        # References
        self.player = player
        self.mikito_group = mikito_group
        self.bullet_group = bullet_group
        self.mikito_bullets = mikito_bullets

        # State
        self.stage = 1
        self.timer = 0
        self.spawn_timer = 0
        self.health = BOSS_HEALTH
        self.transitioning = False
        self.transition_timer = 0
        self.stage2_triggered = False
        self.direction = 1
        self.speed_y = BOSS_SPEED_Y * 5.0
        self.active = True

        # Bullets
        self.cookie_img = pygame.transform.scale(pygame.image.load("assets/cookiebullet.png").convert_alpha(), (100, 100))
        self.bone_img = pygame.transform.scale(pygame.image.load("assets/bonebullet.png").convert_alpha(), (120, 80))

    def update(self, dt):
        """
        Update movement, phase transitions, and attack patterns.

        Args:
            dt (float): Delta time in seconds.
        """
        if not self.active:
            return

        # --- Stage transition ---
        if self.transitioning:
            self.transition_timer += dt
            if self.transition_timer > 0.5:
                self.transitioning = False
                self.image = self.image_stage2
                self.stage = 2
                self.speed_y *= 1.2
            else:
                # Apply a shake effect
                shake = random.randint(-5, 5)
                self.position.x += shake
                self.position.y += shake
                return

        # --- Movement (vertical bounce and horizontal entry) ---
        self.position.y += self.speed_y * self.direction * dt
        upper_bound = 100
        lower_bound = SCREEN_HEIGHT - 100

        if self.position.y < upper_bound:
            self.position.y = upper_bound
            self.direction = 1
        elif self.position.y > lower_bound:
            self.position.y = lower_bound
            self.direction = -1

        if self.position.x > BOSS_ENTRY_X:
            self.position.x -= 100 * dt

        # --- Timers and stage change check ---
        self.timer += dt
        self.spawn_timer += dt

        if self.health <= BOSS_STAGE2_HEALTH and not self.stage2_triggered:
            self.stage2_triggered = True
            self.transitioning = True
            self.transition_timer = 0

        # --- Fire bone bullet every few seconds ---
        if self.timer > 3.5:
            self.timer = 0
            direction = pygame.Vector2(-1, 0)
            bullet = BoneBullet(
                self.position.x - 80,
                self.position.y + BONE_OFFSET_Y,
                direction * 150,
                self.bone_img,
                BONE_DAMAGE
            )
            self.bullet_group.add(bullet)

        # --- Stage 2: fire cookie and spawn Mikitos ---
        if self.stage == 2:
            if random.random() < 0.005:
                direction = pygame.Vector2(-1, 0)
                cookie = CookieBullet(
                    self.position.x - 80,
                    self.position.y + COOKIE_OFFSET_Y,
                    direction * 200,
                    self.cookie_img,
                    COOKIE_DAMAGE,
                    health=3
                )
                self.bullet_group.add(cookie)

            if self.spawn_timer > 5.0:
                self.spawn_timer = 0
                mikito = Enemy(
                    self.position.x - 40,
                    self.position.y,
                    self.player,
                    self.mikito_bullets,
                    dizzy_only=True
                )
                self.mikito_group.add(mikito)

    def take_damage(self, amount):
        """
        Reduce boss health and deactivate if defeated.

        Args:
            amount (int): Damage taken.
        """
        self.health -= amount
        if self.health <= 0:
            self.active = False

    def draw(self, screen):
        """
        Draw the boss, its health bar, and (optionally) hitbox.

        Args:
            screen: Surface to draw on.
        """
        if not self.active:
            return

        image_rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(self.image, image_rect)

        # Draw health bar
        bar_width = 120
        bar_height = 10
        bar_rect = pygame.Rect(image_rect.centerx - bar_width // 2, image_rect.top - 20, bar_width, bar_height)

        if self.health > BOSS_STAGE2_HEALTH:
            fill = ((self.health - BOSS_STAGE2_HEALTH) / BOSS_STAGE1_HEALTH) * bar_width
            pygame.draw.rect(screen, (255, 255, 255), bar_rect, 2)
            pygame.draw.rect(screen, (0, 255, 0), (bar_rect.left, bar_rect.top, fill, bar_height))
        else:
            fill = (self.health / BOSS_STAGE2_HEALTH) * bar_width
            pygame.draw.rect(screen, (255, 255, 255), bar_rect, 2)
            pygame.draw.rect(screen, (255, 0, 0), (bar_rect.left, bar_rect.top, fill, bar_height))

        if SHOW_HITBOXES:
            pygame.draw.rect(screen, (0, 255, 255), self.get_rect(), 2)

# --- Boss Projectile: Bone Bullet ---

class BoneBullet(CircleShape):
    """
    Fast rotating projectile fired by FinalBoss.
    """

    def __init__(self, x, y, velocity, image, damage):
        reduced_radius = int(min(image.get_width(), image.get_height()) * 0.35)
        super().__init__(x, y, reduced_radius)
        self.image = image
        self.velocity = velocity
        self.damage = damage
        self.angle = 0
        self.rotation_speed = 180

    def update(self, dt):
        self.position += self.velocity * dt
        self.angle = (self.angle + self.rotation_speed * dt) % 360

        if self.position.x < -50 or self.position.x > SCREEN_WIDTH + 50:
            self.kill()

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated, rect)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.position.x), int(self.position.y)), self.radius, 1)

# --- Boss Projectile: Cookie Bomb ---

class CookieBullet(CircleShape):
    """
    Slow, durable cookie projectile that takes 3 hits to destroy.
    Only used in FinalBoss Stage 2.
    """

    def __init__(self, x, y, velocity, image, damage, health=3):
        radius = image.get_width() // 2
        super().__init__(x, y, radius)
        self.image = image
        self.velocity = velocity
        self.damage = damage
        self.health = health

    def update(self, dt):
        self.position += self.velocity * dt

        if self.position.x < -50:
            self.kill()

    def draw(self, screen):
        rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(self.image, rect)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, (255, 0, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
