import pygame
from constants import *
from devtools import DEV_MODE, SKIP_TO_LEVEL, GOD_MODE
from enemy import Enemy
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from finalboss import FinalBoss
from screens import show_intro, show_game_over, show_boss_defeated_sequence

# --- Utility Functions ---

def clear_groups(*groups):
    """Kills and clears all sprites from the given groups."""
    for group in groups:
        for sprite in list(group):
            sprite.kill()
        group.empty()

def handle_player_hit(source, player, sound, screen, font):
    """Handles collision between player and a damaging source."""
    source.kill()
    if not player.invincible and not GOD_MODE:
        lost_final_life = player.lose_life()
        sound.play()

        if lost_final_life:
            result = show_game_over(screen, font)
            if result == "restart":
                return True
            pygame.quit()
            exit()
    return False

# --- Main Game Loop ---

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Load Sounds
    shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
    explosion_sound = pygame.mixer.Sound("assets/nomanches.wav")
    gameover_sound = pygame.mixer.Sound("assets/khakha.wav")

    shoot_sound.set_volume(0.4)
    explosion_sound.set_volume(0.7)
    gameover_sound.set_volume(1.0)

    # Setup Screen & Fonts
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 60)

    background_img = pygame.image.load("assets/background.png").convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    life_icon_raw = pygame.image.load("assets/ship.png").convert_alpha()
    life_icon = pygame.transform.scale(life_icon_raw, (24, 24))

    # Game State Initialization
    score = 0
    previous_level = 1
    explosion_cd_player = 0.0

    # Sprite Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    mikito_bullets = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()

    # Class-wide sprite group assignment
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Enemy.containers = (enemies, updatable, drawable)
    AsteroidField.containers = (updatable,)

    # Player and Asteroid Field Initialization
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shoot_sound)
    asteroid_field = AsteroidField(asteroids, enemies, player, mikito_bullets)
    updatable.add(asteroid_field)

    if DEV_MODE:
        asteroid_field.level = SKIP_TO_LEVEL

    show_intro(screen)

    boss = None
    boss_active = False
    boss_defeated = False

    # --- Main Loop ---
    while True:
        dt = clock.tick(60) / 1000
        explosion_cd_player -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.blit(background_img, (0, 0))

        # Update field or trigger boss
        if not boss_active and asteroid_field.level < 10:
            asteroid_field.update(dt)
        elif asteroid_field.level >= 10 and not boss_active:
            boss_active = True
            boss = FinalBoss(player, enemies, boss_bullets, mikito_bullets)
            drawable.add(boss)
            updatable.add(boss)
            updatable.remove(asteroid_field)
            clear_groups(asteroids, enemies, mikito_bullets)
            player.disable_wrap = True

        # Update active objects
        updatable.update(dt)
        mikito_bullets.update(dt)
        boss_bullets.update(dt)

        # Boss defeated
        if boss and boss.health <= 0 and not boss_defeated:
            boss_defeated = True
            player.disable_wrap = False
            show_boss_defeated_sequence(screen)
            result = show_game_over(screen, font, win=True)
            if result == "restart":
                return main()
            pygame.quit()
            exit()

        # Score increase on level up
        if asteroid_field.level > previous_level:
            score += 500
            previous_level = asteroid_field.level

        # --- Collision Handling ---

        # Asteroids vs Player
        for asteroid in list(asteroids):
            distance = player.position.distance_to(asteroid.position)
            if distance < player.radius + asteroid.radius:
                if player.invincible:
                    push = player.position - asteroid.position
                    if push.length() > 0:
                        push.scale_to_length(10)
                        player.position += push
                elif handle_player_hit(asteroid, player, explosion_sound, screen, font):
                    return main()

        # Boss Bullets vs Player
        for bullet in list(boss_bullets):
            hit = (player.position.distance_to(bullet.position) < player.radius + max(bullet.get_rect().width, bullet.get_rect().height) / 2
                   if hasattr(bullet, 'get_rect') else player.collide(bullet))
            if hit and handle_player_hit(bullet, player, explosion_sound, screen, font):
                return main()

        # Mikito Bullets vs Player
        for bullet in list(mikito_bullets):
            if player.collide(bullet):
                if getattr(bullet, 'is_dizzy', False):
                    player.apply_dizzy()
                elif handle_player_hit(bullet, player, explosion_sound, screen, font):
                    return main()
                bullet.kill()

        # Boss vs Player
        if boss and player.collide(boss):
            if not player.invincible and not GOD_MODE:
                lost_final_life = player.lose_life()
                explosion_sound.play()  # ✅ Play sound every time a life is lost

                if lost_final_life:
                    if show_game_over(screen, font) == "restart":
                        return main()
                    pygame.quit()
                    exit()

            else:
                push = player.position - boss.position
                push.x = -abs(push.x) if push.x >= 0 else push.x
                push.y *= 0.3
                if push.length() > 0:
                    push.scale_to_length(30)
                    player.position += push

        # Shots vs Asteroids
        for shot in list(shots):
            for asteroid in list(asteroids):
                if shot.alive() and asteroid.alive() and asteroid.collide(shot):
                    asteroid.split()
                    shot.kill()
                    score += 100
                    break

        # Player vs Enemies & Shots vs Enemies
        for enemy in list(enemies):
            if player.collide(enemy):
                player.push_back_from(enemy.position)

        for shot in list(shots):
            for enemy in list(enemies):
                if shot.alive() and enemy.alive() and enemy.collide(shot):
                    enemy.kill()
                    shot.kill()
                    score += 250
                    break

        # Shots vs Mikito Bullets
        for shot in list(shots):
            for bullet in list(mikito_bullets):
                if shot.alive() and bullet.alive() and bullet.collide(shot):
                    bullet.kill()
                    shot.kill()
                    score += 10
                    break

        # Shots vs Boss Bullets / Boss
        for shot in list(shots):
            for bullet in list(boss_bullets):
                if shot.alive() and bullet.alive() and hasattr(bullet, 'health') and bullet.collide(shot):
                    bullet.health -= 1
                    shot.kill()
                    if bullet.health <= 0:
                        bullet.kill()
                    score += 20

            if boss and shot.alive() and boss.collide(shot):
                boss.take_damage(1)
                shot.kill()
                score += 100

        # --- Drawing Section ---
        for sprite in drawable:
            sprite.draw(screen)
        for bullet in mikito_bullets:
            bullet.draw(screen)
        for bullet in boss_bullets:
            bullet.draw(screen)

        # Draw Arena Walls during Boss Fight
        if boss_active and not boss_defeated:
            wall_color = (255, 100, 100)
            wall_width = 6
            pygame.draw.line(screen, wall_color, (0, 0), (0, SCREEN_HEIGHT), wall_width)
            pygame.draw.line(screen, wall_color, (SCREEN_WIDTH - 1, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT), wall_width)
            pygame.draw.line(screen, wall_color, (0, 0), (SCREEN_WIDTH, 0), wall_width)
            pygame.draw.line(screen, wall_color, (0, SCREEN_HEIGHT - 1), (SCREEN_WIDTH, SCREEN_HEIGHT - 1), wall_width)

        # UI Info
        screen.blit(font.render(f"Level {asteroid_field.level}", True, (255, 255, 0)), (10, 10))
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (SCREEN_WIDTH - 150, 10))
        for i in range(player.lives):
            screen.blit(life_icon, (10 + i * (24 + 5), 40))

        pygame.display.flip()

# --- Entry Point ---
if __name__ == "__main__":
    main()
