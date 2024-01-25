"""Module for particle effects in pygame"""
from random import uniform
from math import pi, cos, sin
from pygame import Surface, sprite, draw, Vector2
from pygame.locals import SRCALPHA
from src.shapes import Circle

class Particles(sprite.Sprite):
    """Particle class for the use of particles in pygame"""
    @staticmethod
    def get_group_dimensions(sprite_group:sprite.Group) -> tuple[int,int]:
        """Get screen space occupied by sprite group members

        :param sprite_group: `sprite group`
        :type sprite_group: sprite.Group
        :return: dimensions of sprite_group `(width,height)`
        :rtype: tuple[int,int]
        """
        width, height = 0, 0
        width = max(particle.rect.left for particle in sprite_group)
        height = max(particle.rect.bottom for particle in sprite_group)
        return (width,height)

    def __init__(self) -> None:
        super().__init__()
        self.particles = []
        self.surface_dimension = (0,0)
        self.image = Surface(self.surface_dimension,SRCALPHA)
        self.rect = None

    def add(self, position:tuple=(0,0), radius=1,
            color:tuple=(255,255,255), outline_width=0) -> None:
        """Add new particle

        :param `position`: coordinate `(x,y)`, defaults to `(0,0)`
        :type position: tuple, optional
        :param `radius`: Circle radius, defaults to `1`
        :type radius: int, optional
        :param `color`: Fill color, defaults to `(255,255,255)`
        :type color: tuple, optional
        :param `outline_width`: Filled width (pixels) from edge. If not used,
            circle will be fully colored., defaults to `0`
        :type outline_width: int, optional
        """
        particle = Circle(position, radius, color, outline_width)
        self.particles.append(particle)


    def update(self, deltatime:float) -> None:
        """Render particles 

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        size = Particles.get_group_dimensions(self.particles)

        if size != self.surface_dimension:
            self.surface_dimension = size
            self.image = Surface(size)
            self.rect = self.image.get_rect()

        self.particles.update(deltatime)
        self.particles.draw(self.image)
        self.image.convert_alpha()
