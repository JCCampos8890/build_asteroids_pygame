# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *

def main():
    # Initialize pygame
    pygame.init()

    # Print starting message and screen size
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")  
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Create the screen (GUI window)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game loop
    while True:
        # Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Exit the game

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Refresh the display
        pygame.display.flip()

if __name__ == "__main__":
    main()

