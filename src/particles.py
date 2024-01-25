"""Module for particle effects in pygame"""
from random import uniform, randint
from math import pi, cos, sin
from pygame import Surface, sprite, draw, Vector2
from pygame.locals import SRCALPHA
from src.shapes import Circle

class Particles():
    """Particle class for the use of particles in pygame"""
    def __init__(self) -> None:
        """Create new particle(s)."""
        self.particles = []

    def draw(self, position:tuple, screen:Surface):
        """Draw particles
        
        General list structure for the particle data is:
        [(x,y), (dx,dy), radius]

        :param particles: 
        :type particles: list
        """
        self.particles.append([position, [randint(0, 30) / 15 - 1, -1], randint(4, 10)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.01
            particle[1][1] += 0.001

            draw.circle(
                screen, (255, 255, 255,90),
                [int(particle[0][0]),int(particle[0][1])],
                int(particle[2])
            )

            if particle[2] <= 0:
                self.particles.remove(particle)




