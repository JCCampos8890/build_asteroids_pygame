import pygame
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from screens import show_intro, show_game_over

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Load sounds
    shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
    explosion_sound = pygame.mixer.Sound("assets/nomanches.wav")
    gameover_sound = pygame.mixer.Sound("assets/khakha.wav")

    # Set volume levels (optional)
    shoot_sound.set_volume(0.4)
    explosion_sound.set_volume(0.7)
    gameover_sound.set_volume(1.0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    life_icon = pygame.image.load("assets/ship.png").convert_alpha()
    icon_size = 24
    life_icon = pygame.transform.scale(life_icon, (icon_size, icon_size))

    show_intro(screen, font)

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shoot_sound)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField(asteroids)

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    explosion_cd_player = 0.0  # Player collision sound cooldown

    # Game loop
    while True:
        dt = clock.tick(60) / 1000
        explosion_cd_player -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        updatable.update(dt)

        # PLAYER vs ASTEROID
        for asteroid in list(asteroids):
            if not player.invincible and player.collide(asteroid):
                if explosion_cd_player <= 0:
                    explosion_sound.play()
                    explosion_cd_player = 0.5

                if player.lose_life():
                    gameover_sound.play()
                    show_game_over(screen, font)
                    return main()

        # SHOT vs ASTEROID (no sound)
        for shot in list(shots):
            for asteroid in list(asteroids):
                if not shot.alive() or not asteroid.alive():
                    continue

                if asteroid.collide(shot):
                    asteroid.split()
                    shot.kill()
                    break  # prevent double collision

        # DRAW
        for sprite in drawable:
            sprite.draw(screen)

        level_text = font.render(f"Level {asteroid_field.level}", True, (255, 255, 0))
        screen.blit(level_text, (10, 10))

        for i in range(player.lives):
            screen.blit(life_icon, (10 + i * (icon_size + 5), 40))

        pygame.display.flip()

if __name__ == "__main__":
    main()
