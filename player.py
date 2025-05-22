import pygame
import math
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, shoot_sound):
        # Load images
        self.ship_img = pygame.image.load("assets/ship.png").convert_alpha()
        self.ship_flame_img = pygame.image.load("assets/shipflame.png").convert_alpha()
        self.ship_flame_img_dizzy = pygame.image.load("assets/shipflame_dizzy.png").convert_alpha()

        diameter = PLAYER_RADIUS * 4  

        self.ship_img = pygame.transform.scale(self.ship_img, (diameter, diameter))
        self.ship_flame_img = pygame.transform.scale(self.ship_flame_img, (diameter, diameter))
        self.ship_flame_img_dizzy = pygame.transform.scale(self.ship_flame_img_dizzy, (diameter, diameter)) 

        self.image = self.ship_img
        
        self.ship_img_red = self._tint_image(self.ship_img, (255, 80, 80))
        self.ship_flame_img_red = self._tint_image(self.ship_flame_img, (255, 80, 80))

        visual_radius = diameter // 2.1
        super().__init__(x, y, visual_radius)

        self.rotation = 0
        self.timer = 0.0
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 200
        self.friction = 0.98
        self.max_speed = 400
        self.lives = 3

        self.invincible = False
        self.invincibility_timer = 0.0

        self.shoot_sound = shoot_sound

        self.dizzy = False
        self.dizzy_timer = 0.0

    def _tint_image(self, image, tint_color):
        tinted = image.copy()
        tint_surface = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        tint_surface.fill(tint_color + (0,))
        tinted.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted

    def draw(self, screen):
    # Choose base flame image
        if self.image == self.ship_flame_img or self.image == self.ship_flame_img_dizzy:
            if self.dizzy:
                base_image = self.ship_flame_img_dizzy
                red_image = self._tint_image(base_image, (255, 80, 80))
            else:
                base_image = self.ship_flame_img
                red_image = self.ship_flame_img_red
        else:
            base_image = self.ship_img
            red_image = self.ship_img_red

        # Handle invincibility blink effect
        if self.invincible:
            blink = (pygame.time.get_ticks() // 100) % 2 == 0
            image_to_draw = red_image if blink else base_image
        else:
            image_to_draw = base_image

        # Handle dizzy wobble
        if self.dizzy:
            wobble_offset = 5 * math.sin(pygame.time.get_ticks() / 100)
            rotated_image = pygame.transform.rotate(image_to_draw, -self.rotation + wobble_offset)
        else:
            rotated_image = pygame.transform.rotate(image_to_draw, -self.rotation)


        rect = rotated_image.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_image, rect)


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Handle dizzy effect
        if self.dizzy:
            self.dizzy_timer -= dt
            if self.dizzy_timer <= 0:
                self.dizzy = False

        left = pygame.K_LEFT
        right = pygame.K_RIGHT
        up = pygame.K_UP

        if self.dizzy:
            left, right = right, left  # Invert controls when dizzy

        if keys[left]:
            self.rotate(-dt)
        if keys[right]:
            self.rotate(dt)

        if keys[up]:
            thrust = pygame.Vector2(0, -1).rotate(self.rotation)
            self.velocity += thrust * self.acceleration * dt

        # Always assign image based on dizzy state and thrusting
        if self.dizzy:
            self.image = self.ship_flame_img_dizzy
        elif keys[up]:
            self.image = self.ship_flame_img
        else:
            self.image = self.ship_img

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * dt
        self.velocity *= self.friction

        if self.timer > 0:
            self.timer -= dt

        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()
            self.timer = PLAYER_SHOOT_COOLDOWN

        if self.invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.invincible = False

        self.wrap_position()

    def shoot(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        velocity = forward * PLAYER_SHOOT_SPEED
        spawn_position = self.position + forward * self.radius
        Shot(spawn_position.x, spawn_position.y, velocity)
        self.shoot_sound.play()

    def lose_life(self):
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
        self.dizzy = True
        self.dizzy_timer = duration
        pygame.mixer.Sound("assets/iugh.wav").play()

    def push_back_from(self, source_position, force=8):
        direction = self.position - source_position
        if direction.length() > 0:
            direction = direction.normalize()
            self.velocity += direction * force
