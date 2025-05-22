import pygame
from constants import *
from enemy import Enemy
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

    shoot_sound.set_volume(0.4)
    explosion_sound.set_volume(0.7)
    gameover_sound.set_volume(1.0)

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    # Lives icon
    life_icon_raw = pygame.image.load("assets/ship.png").convert_alpha()
    icon_size = 24
    life_icon = pygame.transform.scale(life_icon_raw, (icon_size, icon_size))

    # Game state
    score = 0
    previous_level = 1
    explosion_cd_player = 0.0

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    mikito_bullets = pygame.sprite.Group()

    # Assign containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Enemy.containers = (enemies, updatable, drawable)
    AsteroidField.containers = (updatable,)

    # Initialize objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shoot_sound)
    asteroid_field = AsteroidField(asteroids, enemies, player, mikito_bullets)

    # Show intro screen
    show_intro(screen)

    # Main game loop
    while True:
        dt = clock.tick(60) / 1000
        explosion_cd_player -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))

        # Update
        asteroid_field.update(dt)
        updatable.update(dt)
        mikito_bullets.update(dt)

        # Check level bonus
        if asteroid_field.level > previous_level:
            score += 500
            previous_level = asteroid_field.level

        # Player vs Asteroid
        for asteroid in list(asteroids):
            if player.collide(asteroid):
                if not player.invincible:
                    if explosion_cd_player <= 0:
                        explosion_sound.play()
                        explosion_cd_player = 0.5
                    asteroid.kill()
                    if player.lose_life():
                        gameover_sound.play()
                        show_game_over(screen, font)
                        return main()
                else:
                    push = player.position - asteroid.position
                    if push.length() > 0:
                        push.scale_to_length(5)
                        player.position += push

        # Mikito bullet vs Player
        for bullet in list(mikito_bullets):
            if player.collide(bullet):
                player.apply_dizzy()
                bullet.kill()

        # Shot vs Asteroid
        for shot in list(shots):
            for asteroid in list(asteroids):
                if not shot.alive() or not asteroid.alive():
                    continue
                if asteroid.collide(shot):
                    asteroid.split()
                    shot.kill()
                    score += 100
                    break

        # Player vs Enemy
        for enemy in list(enemies):
            if player.collide(enemy):
                player.push_back_from(enemy.position)

        # Shot vs Enemy
        for shot in list(shots):
            for enemy in list(enemies):
                if shot.alive() and enemy.alive() and enemy.collide(shot):
                    enemy.kill()
                    shot.kill()
                    score += 250
                    break

        # Draw
        for sprite in drawable:
            sprite.draw(screen)
        for bullet in mikito_bullets:
            bullet.draw(screen)

        # HUD
        level_text = font.render(f"Level {asteroid_field.level}", True, (255, 255, 0))
        screen.blit(level_text, (10, 10))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        for i in range(player.lives):
            screen.blit(life_icon, (10 + i * (icon_size + 5), 40))

        pygame.display.flip()

if __name__ == "__main__":
    main()
