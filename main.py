import pygame
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
import sys
from shot import Shot


def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0


    # Create sprite groups for updatable and drawable objects   
    updatable = pygame.sprite.Group()    
    drawable = pygame.sprite.Group()   
    Player.containers = (updatable, drawable)   # Set up containers for the Player class
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)    # Create player instance

    # Create asteroid field and add it to the updatable group
    asteroids = pygame.sprite.Group()           # Create a group for asteroids
    Asteroid.containers = (asteroids, updatable, drawable)# Set up containers for the Asteroid class    
    AsteroidField.containers = (updatable,)      # Set up containers for the AsteroidField class
    asteroid_field = AsteroidField()           # Create asteroid field instance
    
    # Create shots group and set up containers for the Shot class    
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    
    # Main game loop    
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))          # Fill screen with black
        updatable.update(dt)           # Update all objects

        for asteroid in asteroids:      # Check for collisions with asteroids
            if player.collide(asteroid):
                sys.exit("💀 Game Over! The asteroid didn’t move... but you did.")

        for sprite in drawable:        # Draw all drawable objects
            sprite.draw(screen)

        for asteroid in asteroids:      # Check for collisions between asteroids
            for shot in shots:
                if asteroid.collide(shot):
                    asteroid.split()
                    shot.kill() 


        pygame.display.flip()          # Refresh the display
        dt = clock.tick(60) / 1000     # Maintain 60 FPS and get delta time


if __name__ == "__main__":
    main()

