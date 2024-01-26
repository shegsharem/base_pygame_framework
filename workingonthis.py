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
from src.collisions import check_collision_with_sprite_group
from src.lighting import get_outline
from src.particles import Particles
#from src.curves import mesh

pygame.init()

screen = pygame.display.set_mode((1280,720), DOUBLEBUF)
previous_time = get_deltatime()

test_rect = Rectangle((0,0),(50,50), (0,0,0))

player = Player()
player_outline = get_outline(player.image)

level_surface = pygame.Surface((1280*2,720*2), SRCALPHA)
level = Level('level.txt')
level.draw(level_surface)

splashscreen = pygame.image.load('assets/images/background.png').convert_alpha()
splashscreen = pygame.transform.scale(splashscreen, (screen.get_width(), screen.get_height()))

#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) # allows certain inputs to increase performance
particles = Particles()

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
        test_rect.position.y -= 2

    if keys[K_d]:
        test_rect.position.x += 1
    
    if keys[K_a]:
        test_rect.position.x -= 1

while True:
    dt, previous_time = get_deltatime(previous_time)
    input_processor()
    mouse_pos = pygame.mouse.get_pos()
    
    #player.position = mouse_pos

    test_rect.update(0)
    player.update(dt)

    screen.blit(splashscreen,(0,0))
    screen.blit(level_surface,(0,0))
    screen.blit(test_rect.image,test_rect.position)
    collisions = check_collision_with_sprite_group(test_rect,level)
    print(collisions)
    if not collisions['bottom']:
        test_rect.position.y += 1
    screen.blit(player_outline,player.position)
    screen.blit(player.image,player.position)


    pygame.display.flip()
