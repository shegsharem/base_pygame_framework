"""Python 3.12.1"""
from pygame import Vector2, draw, sprite, Color, Surface
from pygame.locals import *

class Circle(sprite.Sprite):
    """Simple circle shape class for pygame"""
    def __init__(self,radius=1,color:tuple=(255,255,255),outline_width=0) -> None:
        super().__init__()
        self.image = Surface([radius*2,radius*2],SRCALPHA)
        self.rect = self.image.get_rect()
        self.position = Vector2(self.rect.topleft)
        self.direction = Vector2(1,0)
        self.speed = 400
        self.color = Color(color[0],color[1],color[2])
        self.radius = radius
        self.outline_width = outline_width
        # Draw circle on self.image
        draw.circle(self.image, self.color, self.position, self.radius, self.outline_width)

    def update(self, deltatime:float) -> None:
        """Circle update method 

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.position += (self.direction*self.speed*deltatime)
        #self.position.x -= self.radius
        #self.position.y -= self.radius
        self.rect.topleft = round(self.position.x), round(self.position.y)


class Rectangle(sprite.Sprite):
    """Simple rectangle shape class for pygame"""
    def __init__(self,position:tuple=(0,0),dimensions:tuple=(10,10),
                 color:tuple=(255,255,255)) -> None:
        super().__init__()
        self.image = Surface(dimensions,SRCALPHA)
        self.rect = self.image.get_rect()
        self.position = Vector2(self.rect.topleft)
        self.direction = Vector2(1,0)
        self.speed = 400
        self.color = Color(color[0],color[1],color[2])
        # Draw rectangle on self.image
        draw.rect(self.image, self.color, self.rect)

    def update(self, deltatime:float) -> None:
        """Rectangle update method 

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.position += (self.direction*self.speed*deltatime)
        self.rect.topleft = round(self.position.x), round(self.position.y)
