import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from shot import Shot  

# Player class that represents the spaceship
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0.0

    # Returns the three points of the triangle
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # Draws the triangle on the screen
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), width=2)

    # Rotates the player
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # Updates the player position and rotation based on key presses
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.position += forward * PLAYER_SPEED * dt
        if keys[pygame.K_DOWN]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.position -= forward * PLAYER_SPEED * dt 

        # Cooldown logic
        if self.timer > 0:
            self.timer -= dt

        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()
            self.timer = PLAYER_SHOOT_COOLDOWN  # reset timer

    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        Shot(self.position.x, self.position.y, velocity)