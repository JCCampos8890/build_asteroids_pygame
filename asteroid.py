import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

# Tier system for asteroid sizes
TIERS = [50, 20, 10]  # Large, Medium, Small

class Asteroid(CircleShape):
    def __init__(self, x, y, base_radius):
        self.base_radius = base_radius  # Save tier-based radius
        original_image = pygame.image.load("assets/asteroid.png").convert_alpha()
        self.wrap_count = 0  # Track how many times it wrapped

        # Init physics
        super().__init__(x, y, base_radius)

        # Visual scaling
        visual_scale = 3.5
        diameter = base_radius * visual_scale
        self.image = pygame.transform.scale(original_image, (int(diameter), int(diameter)))
        self.radius = diameter // 2.2  # For collision logic

        # Rotation
        self.rotation = 0
        self.rotation_speed = random.uniform(-90, 90)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_image, rect)

        # test draw hitbox
        #pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), self.radius, 1)

    def update(self, dt):
        self.rotation += self.rotation_speed * dt
        self.position += self.velocity * dt
        old_position = self.position.copy()
        self.wrap_position()

        # If it wrapped (position changed sides), count it
        # and kill if it wrapped 3 times        
        if old_position.x != self.position.x or old_position.y != self.position.y:
            self.wrap_count += 1
            if self.wrap_count >= 3:
                self.kill()


    def split(self):
        self.kill()

        # Don't split if size not recognized
        if self.base_radius not in TIERS:
            return

        current_index = TIERS.index(self.base_radius)
        if current_index + 1 >= len(TIERS):
            return  

        new_radius = TIERS[current_index + 1]

        angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(angle) * 1.2
        v2 = self.velocity.rotate(-angle) * 1.2
        x, y = self.position.x, self.position.y

        Asteroid(x, y, new_radius).velocity = v1
        Asteroid(x, y, new_radius).velocity = v2
