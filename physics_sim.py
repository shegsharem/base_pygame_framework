import sys
import time
import pygame
from pygame.locals import *
from src.circle import Circle

pygame.init()
screen = pygame.display.set_mode((640,390),pygame.HWSURFACE|pygame.DOUBLEBUF)

clock = pygame.time.Clock()
#player = Player() when player is external file
FPS = 60

particles = pygame.sprite.Group()
circle = Circle((255,0,255),(100,100),100,0)
particles.add(circle)

def main():
    running = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        particles.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
