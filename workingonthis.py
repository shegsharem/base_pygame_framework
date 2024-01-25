# pylint: disable=maybe-no-member
import sys
from random import randint
import pygame
from pygame.locals import *

# Game Modules
from src.shapes import Circle, Rectangle
from src.deltatime import get_deltatime
from src.player import Player
from src.level import Level
from src.collisions import intersecting_rect_with_sprite_group
from src.lighting import get_outline
from src.particles import Particles
#from src.curves import mesh

pygame.init()

screen = pygame.display.set_mode((1280,720), DOUBLEBUF)
previous_time = get_deltatime()

test_rect = Rectangle((0,0),(50,50), (0,0,0))

test_rect_outline = get_outline(test_rect.image)
#player = Player()
level_map = list(open('level.txt'))

background = Level(level_map)
level_terrain = background.render_terrain(screen)
level_outline = get_outline(level_terrain)
splashscreen = pygame.image.load('assets/images/background.png').convert_alpha()
splashscreen = pygame.transform.scale(splashscreen, (screen.get_width(), screen.get_height()))

particles = Particles()
#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) # allows certain inputs to increase performance


def input_processor() -> None:
    """Logic function for pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if keys[K_w]:
        pass
        #player.sprite_number += 1
        #player.acceleration.y = -2
        #player.touching_ground = True

while True:
    dt, previous_time = get_deltatime(previous_time)

    print(dt)
    input_processor()

    mouse_pos = pygame.mouse.get_pos()

    particles.add_particle((mouse_pos[0]+randint(-10,10),mouse_pos[1]+randint(-10,10)),6)

    test_rect.position = mouse_pos

    test_rect.update(dt)
    particles.update(dt)
    #player.update(dt)

    screen.blit(splashscreen,(0,0))
    #screen.blit(level_terrain,(0,0))
    screen.blit(level_outline,(0,0))
    particles.draw(screen)

    screen.blit(test_rect.image,test_rect.position)
    screen.blit(test_rect_outline,test_rect.position)
    

    #screen.blit(player.image,player.position)

    pygame.display.flip()
