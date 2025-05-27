"""
Handles static and animated screen transitions such as:
- Game intro screen
- Game over screen
- Boss defeated cinematic sequence
"""

import pygame
import time
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


# --- STATIC SCREENS ---

def show_intro(screen):
    """
    Display the intro screen and wait for the player to press Enter.
    """
    _show_static_screen(screen, "assets/opening.png", wait_for="enter")


def show_game_over(screen, font, win=False):
    """
    Display the game over screen.

    Args:
        screen: The display surface.
        font: The font to use for rendering text.
        win (bool): Whether the player won or lost.

    Returns:
        str or None: Returns 'restart' if R is pressed or Q to exit.
    """
    return _show_static_screen(screen, "assets/gameover.png", wait_for="r_or_q")


def _show_static_screen(screen, image_path, wait_for="enter"):
    """
    Displays a static image screen with optional key trigger.

    Args:
        screen: The display surface.
        image_path (str): Path to the image.
        wait_for (str): Expected key trigger. Options: 'enter', 'r_or_q'

    Returns:
        str or None: 'restart' if R pressed, otherwise None.
    """
    clock = pygame.time.Clock()

    # Load and scale the image to fit the screen
    image = pygame.image.load(image_path).convert()
    screen_rect = screen.get_rect()
    img_rect = image.get_rect()

    scale = min(screen_rect.width / img_rect.width, screen_rect.height / img_rect.height)
    new_size = (int(img_rect.width * scale), int(img_rect.height * scale))
    image = pygame.transform.scale(image, new_size)
    img_rect = image.get_rect(center=screen_rect.center)

    # Wait for input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

            elif event.type == pygame.KEYDOWN:
                if wait_for == "enter" and event.key == pygame.K_RETURN:
                    return
                elif wait_for == "r_or_q":
                    if event.key == pygame.K_r:
                        return "restart"
                    elif event.key == pygame.K_q:
                        pygame.quit(); exit()

        screen.fill((0, 0, 0))
        screen.blit(image, img_rect)
        pygame.display.flip()
        clock.tick(60)


# --- BOSS DEFEATED SEQUENCE ---

def show_boss_defeated_sequence(screen):
    """
    Display a 2-part cinematic sequence when the player defeats the final boss.
    """
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 72, bold=True)

    screen_width, screen_height = screen.get_size()

    # Load and scale images
    boss_defeated_img = pygame.image.load("assets/boss_defeated.png").convert_alpha()
    boss_illback_img = pygame.image.load("assets/boss_illback.png").convert_alpha()
    scale_width = int(screen_width * 0.4)

    def scale_and_center(image):
        aspect_ratio = image.get_height() / image.get_width()
        scaled = pygame.transform.smoothscale(image, (scale_width, int(scale_width * aspect_ratio)))
        return scaled, scaled.get_rect(center=(screen_width // 2, screen_height // 2))

    boss_defeated_img, defeated_rect = scale_and_center(boss_defeated_img)
    boss_illback_img, illback_rect = scale_and_center(boss_illback_img)

    def fade_in(image, rect, text, color):
        alpha = 0
        overlay = pygame.Surface((screen_width, screen_height)).convert()
        overlay.fill((0, 0, 0))

        while alpha < 255:
            screen.fill((0, 0, 0))
            screen.blit(image, rect)
            overlay.set_alpha(255 - alpha)
            screen.blit(overlay, (0, 0))

            # Draw text
            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect(center=(screen_width // 2, rect.top - 40))
            screen.blit(text_surf, text_rect)

            pygame.display.flip()
            clock.tick(60)
            alpha += 8

    def hold(image, rect, text, color, duration):
        start = time.time()
        while time.time() - start < duration:
            screen.fill((0, 0, 0))
            screen.blit(image, rect)

            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect(center=(screen_width // 2, rect.top - 40))
            screen.blit(text_surf, text_rect)

            pygame.display.flip()
            clock.tick(60)

    # Sequence: YOU WIN! > I WILL BE BACK!
    fade_in(boss_defeated_img, defeated_rect, "YOU WIN!", (255, 215, 0))         # gold
    hold(boss_defeated_img, defeated_rect, "YOU WIN!", (255, 215, 0), 3)

    fade_in(boss_illback_img, illback_rect, "...but I WILL BE BACK!", (255, 50, 100))  # magenta-red
    hold(boss_illback_img, illback_rect, "...but I WILL BE BACK!", (255, 50, 100), 3)
