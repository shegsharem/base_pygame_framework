"""Python 3.12.1"""
from pygame import Surface, Vector2, draw, sprite

class Circle(sprite.Sprite):
    """Generic circle sprite to be used in pygame projects"""
    def __init__(self, color=(255,255,255), position=(0,0), radius=1, outline_width=0) -> None:
        """Create new circle

        :param `color`: Fill color, defaults to `(255,255,255)`
        :type color: tuple, optional
        :param `position`: Center coordinate, defaults to `(0,0)`
        :type position: tuple, optional
        :param `radius`: Circle radius, defaults to `1`
        :type radius: int, optional
        :param `outline_width`: Filled width (pixels) from edge. If not used,
            circle will be fully colored., defaults to `0`
        :type outline_width: int, optional
        """
        super().__init__()

        self.color = color
        self.position = Vector2(position[0],position[1])
        self.radius = radius
        self.outline_width = outline_width

        self.image = Surface([self.radius*2, self.radius*2])

        draw.circle(
            self.image,
            self.color,
            self.position,
            self.radius,
            self.outline_width
        )

        self.rect = self.image.get_rect()
