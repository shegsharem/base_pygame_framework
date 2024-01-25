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
        self.particles.append([position, [randint(-1,1)/900, randint(-1,1)/900], randint(3, 9)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.013
            
            particle[1][0] += randint(-1,1)/450
            particle[1][1] += randint(-1,1)/450

            draw.circle(
                screen, (255, 100, 10,255),
                [int(particle[0][0]),int(particle[0][1])],
                int(particle[2])
            )

            particle[1][0] += randint(-1,1)/450
            particle[1][1] += randint(-1,1)/450
            particle[2] -= 0.013

            draw.circle(
                screen, (255, 0, 10,255),
                [int(particle[0][0]),int(particle[0][1])],
                int(particle[2])
            )

            if particle[2] <= 0:
                self.particles.remove(particle)



