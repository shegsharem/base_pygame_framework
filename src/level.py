"""Level loader"""
from pygame import sprite, Surface, image, transform
from pygame.locals import SRCALPHA

class Dirt(sprite.Sprite):
    """Dirt sprite"""
    def __init__(self) -> None:
        super().__init__()
        __scale = (36,36)
        __path = "assets/images/dirt.png"
        self.image = Surface(__scale,SRCALPHA)
        self.dirt = transform.scale(image.load(__path).convert_alpha(), __scale)
        self.image.blit(self.dirt,(0,0))
        self.rect = self.image.get_bounding_rect()


class Grass(sprite.Sprite):
    """Grass sprite"""
    def __init__(self, type:str=None) -> None:
        super().__init__()
        __scale = (36,36)
        __path = "assets/images/grass.png"
        if type == 'left':
            __path = "assets/images/grass_left.png"
        if type == 'right':
            __path = "assets/images/grass_right.png"
        self.image = Surface(__scale,SRCALPHA)
        self.grass = transform.scale(image.load(__path).convert_alpha(), __scale)
        self.image.blit(self.grass,(0,0))
        self.rect = self.image.get_bounding_rect()


class Level(sprite.Group):
    """Main level class"""
    def __init__(self, mapfilepath:str) -> None:
        """Create new level instance

        :param mapfilepath: `filepath` for level map
        :type mapfilepath: str
        """
        super().__init__()

        # Read level map file ###########################
        with open(mapfilepath, encoding="utf-8") as file:
            __tilemap = list(file)
        #################################################

        for row_index, row in enumerate(__tilemap):
            for col_index, cell in enumerate(row):
                if cell == "D":
                    dirt = Dirt()
                    dirt.rect.topleft = (
                        -36+int(col_index*36),
                        -36+int(row_index*36))
                    self.add(dirt)

                if cell == "G":
                    grass = Grass()
                    grass.rect.topleft = (
                        -36+int(col_index*36),
                        -36+int(row_index*36))
                    self.add(grass)

                if cell == "F":
                    grass = Grass('left')
                    grass.rect.topleft = (
                        -36+int(col_index*36),
                        -36+int(row_index*36))
                    self.add(grass)

                if cell == "H":
                    grass = Grass('right')
                    grass.rect.topleft = (
                        -36+int(col_index*36),
                        -36+int(row_index*36))
                    self.add(grass)

                if cell == " ":
                    pass
