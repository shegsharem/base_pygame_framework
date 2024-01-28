""" python 3.12.1 """
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

screen = pygame.display.set_mode((1280,720), DOUBLEBUF|HWSURFACE)
previous_time = get_deltatime()

player = Player()
player.speed = 500

level_surface = pygame.Surface((1280*2,720*2), SRCALPHA)
level = Level('level.txt')
level.draw(level_surface)

splashscreen = pygame.image.load('assets/images/background.png').convert_alpha()
splashscreen = pygame.transform.scale(splashscreen, (screen.get_width(), screen.get_height()))

#pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP]) # allows certain inputs to increase performance
particles = Particles()

while True:
    dt, previous_time = get_deltatime(previous_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update(dt,level)
    screen.blit(splashscreen,(0,0))
    screen.blit(level_surface,(0,0))

    screen.blit(player.image,player.position)

    pygame.display.flip()
