import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

# Shot class that represents the shots fired by the player
class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = velocity

    # Draws the shot on the screen
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius)

    # Updates the shot position
    def update(self, dt):
        self.position += self.velocity * dt