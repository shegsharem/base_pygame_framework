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
        self.particles.append([position, [randint(-1,1)/900, -0.25], randint(3, 9)])
        red = 255
        green = 80
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.0125
            if red < 200:
                red -= 0.01
            if green > 100:
                green += 2
            #particle[1][1] -= 0.001

            draw.circle(
                screen, (red, green, 10,255),
                [int(particle[0][0]),int(particle[0][1])],
                int(particle[2])
            )

            if particle[2] <= 0:
                self.particles.remove(particle)




