"""Module for particle effects in pygame"""
from random import uniform
from math import pi, cos, sin
from pygame import Surface, sprite, draw, Vector2
from pygame.locals import SRCALPHA

class Particle(sprite.Sprite):
    """Generic particle class for pygame"""
    def __init__(self, position=(0,0), radius=1) -> None:
        """Create particle instance

        :param position: `(x,y)`, defaults to `(0,0)`
        :type position: tuple, optional
        :param radius: `particle radius`, defaults to `1`
        :type radius: int, optional
        """
        super().__init__()
        self.position = Vector2((position[0]+radius, position[1]+radius))
        self.velocity = Vector2(uniform(0.5,1.5),uniform(0.5,1.5))
        self.radius = radius
        self.theta = uniform(0,2*pi)
        self.image = Surface([radius*2, radius*2])
        self.rect = self.image.get_rect()

        # Draw particle on self.image
        draw.circle(self.image, (255,255,255), self.position, self.radius)
        self.image.convert_alpha()

    def move(self, deltatime:float) -> None:
        """Move particle

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.theta += 100
        self.velocity *= (cos(self.theta), sin(self.theta)

        self.position += (
            cos(self.theta)*self.velocity.x*deltatime,
            sin(self.theta)*self.velocity.y*deltatime
        )

        self.position.x -= self.radius
        self.position.y -= self.radius
        
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def update(self, deltatime:float) -> None:
        """Particle update method

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.move(deltatime)

class Particles(sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        pass

    def add_particle(self, position=(0,0), radius=1) -> None:
        self.add(Particle(position, radius))
