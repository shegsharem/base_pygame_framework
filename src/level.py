"""Level loader"""
from pygame import sprite, Surface

class Level:
    """Level class. Block sprites shall be 5x5px"""
    def __init__(self, level_map:list) -> None:
        self.level_map = level_map
        self.group = sprite.Group()

        for row_index, row in enumerate(self.level_map):
            for col_index, cell in enumerate(row):
                x = -10 + int(col_index*10)
                y = -10 + int(row_index*10)

                # Dirt
                if cell == "D":
                    self.terrain = sprite.Sprite()
                    self.terrain.image = Surface((10,10))
                    self.terrain.rect = self.terrain.image.get_rect().move(x,y)
                    self.group.add(self.terrain)

                if cell == " ":
                    pass

    def update(self, screen:Surface):
        for tile in self.group:
            screen.blit(tile.image, tile.rect)
