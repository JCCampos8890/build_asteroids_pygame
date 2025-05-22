import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def show_intro(screen):
    _show_static_screen(screen, "assets/opening.png", wait_for="enter")

def show_game_over(screen, font):
    _show_static_screen(screen, "assets/gameover.png", wait_for="r_or_q")

def _show_static_screen(screen, image_path, wait_for="enter"):
    clock = pygame.time.Clock()

    # Load and scale image to fit screen
    image = pygame.image.load(image_path).convert()
    screen_rect = screen.get_rect()
    img_rect = image.get_rect()

    scale = min(screen_rect.width / img_rect.width, screen_rect.height / img_rect.height)
    new_size = (int(img_rect.width * scale), int(img_rect.height * scale))
    image = pygame.transform.scale(image, new_size)
    img_rect = image.get_rect(center=screen_rect.center)

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
        clock.tick(60)  # prevent flickering
