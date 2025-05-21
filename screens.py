import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def show_intro(screen, font):
    screen.fill((0, 0, 0))
    title = font.render("🚀 Love & Asteroids", True, (255, 255, 255))
    instructions = font.render("Arrow keys to move | Space to shoot", True, (200, 200, 200))
    prompt = font.render("Press ENTER to start", True, (100, 255, 100))

    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 60)))
    screen.blit(instructions, instructions.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
    screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40)))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def show_game_over(screen, font):
    screen.fill((0, 0, 0))
    title = font.render("💥 Game Over!", True, (255, 0, 0))
    prompt = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20)))
    screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit(); exit()
