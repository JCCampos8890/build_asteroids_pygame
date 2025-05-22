import pygame
import random
from circleshape import CircleShape
from constants import ENEMY_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(CircleShape):
    def __init__(self, x, y, player, bullet_group):
        image = pygame.image.load("assets/mikito.png").convert_alpha()
        diameter = ENEMY_RADIUS * 3.2
        self.image = pygame.transform.scale(image, (int(diameter), int(diameter)))

        super().__init__(x, y, diameter // 2.2)

        self.player = player
        self.bullet_group = bullet_group
        self.speed = 40
        self.shoot_timer = random.uniform(3.0, 5.0)
        self.rotation = 0

    def update(self, dt):
        # Tracking logic
        if self.player:
            direction = self.player.position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * self.speed * dt

                # rotate Mikito to face the player
                self.rotation = direction.angle_to(pygame.Vector2(0, -1))

        # Shooting logic
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = random.uniform(3.0, 5.0)

        self.wrap_position()

    def shoot(self):
        direction = self.player.position - self.position
        if direction.length() == 0:
            return
        direction = direction.normalize()
        bullet = EnemyBullet(self.position.x, self.position.y, direction * 120)
        self.bullet_group.add(bullet)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_image, rect)


class EnemyBullet(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, 6)
        self.velocity = velocity

        # Load poop bomb image
        self.image = pygame.image.load("assets/mikitoshot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (24, 24))  # Adjust if needed

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()

        # Kill bullet if way off-screen
        if (self.position.x < -50 or self.position.x > SCREEN_WIDTH + 50 or
            self.position.y < -50 or self.position.y > SCREEN_HEIGHT + 50):
            self.kill()

    def draw(self, screen):
        rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(self.image, rect)
