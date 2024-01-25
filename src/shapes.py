"""Python 3.12.1"""
from pygame import Surface, Vector2, draw, sprite, Color
from pygame.locals import *

class Circle(sprite.Sprite):
    """Simple circle shape class for pygame"""
    def __init__(self, position:tuple=(0,0), radius=1,
                 color:tuple=(255,255,255), outline_width=0) -> None:
        """Create circle instance

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
        super().__init__()
        self.position = Vector2(position[0]+radius,position[1]+radius)
        self.velocity = Vector2(0,0)
        self.color = Color(color[0],color[1],color[2])
        self.radius = radius
        self.outline_width = outline_width
        self.image = Surface([radius*2, radius*2],SRCALPHA)
        self.rect = self.image.get_rect()

        # Draw circle on self.image
        draw.circle(self.image, self.color, self.position, self.radius, self.outline_width)

    def move(self, deltatime:float) -> None:
        """Move circle

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.position += (self.velocity*deltatime)
        self.position.x -= self.radius
        self.position.y -= self.radius
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def update(self, deltatime:float) -> None:
        """Circle update method 

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.move(deltatime)


class Rectangle(sprite.Sprite):
    """Simple rectangle shape class for pygame"""
    def __init__(self, position:tuple=(0,0), dimensions:tuple=(10,10),
                 color:tuple=(255,255,255)) -> None:
        """Create rectangle instance

        :param position: coordinate `(x,y)`, defaults to `(0,0)`
        :type position: tuple, optional
        :param dimensions: rectangle size `(width,height)`, defaults to `(10,10)`
        :type dimensions: tuple, optional
        :param color: fill color `(r,g,b)`, defaults to `(255,255,255)`
        :type color: tuple, optional
        """
        super().__init__()
        self.position = Vector2(position[0], position[1])
        self.velocity = Vector2(0,0)
        self.color = Color(color[0], color[1], color[2])
        self.image = Surface(dimensions, SRCALPHA)
        self.rect = self.image.get_rect()

        # Draw rectangle on self.image
        draw.rect(self.image, self.color, self.rect)

    def move(self, deltatime:float) -> None:
        """Move rectangle

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.position += (self.velocity*deltatime)
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def update(self, deltatime:float) -> None:
        """Rectangle update method 

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        self.move(deltatime)
