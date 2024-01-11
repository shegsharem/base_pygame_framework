""" python 3.12.1 """
from pygame import sprite, image, mask, transform

class Player(sprite.Sprite):
    """Player class for game"""
    def __init__(self, start_position:tuple=(0,0),
                 image_path:str=None,
                 number_of_sprites:int=1) -> None:
        super().__init__()
        self.position = start_position
        self.sprite_list = []
        self.sprite_number = 0

        for i in range(number_of_sprites):
            self.sprite_list.append(image_path + str(i) + '.png')

        self.image = image.load(self.sprite_list[self.sprite_number]).convert_alpha()
        self.rect = self.image.get_rect()

        self.mask = None
        self.mask_rect = None

    def move(self, position:tuple=None) -> None:
        """Update player position

        Args: position (tuple, optional): Change in position (vector form). Defaults to None.
        """
        self.rect.move_ip(position)

    def change_sprite_number(self, sprite_number:int) -> None:
        """Change sprite number

        Args:
            sprite_number (int): sprite number in list
        """
        self.sprite_number = sprite_number
        self.image = image.load(self.sprite_list[self.sprite_number]).convert_alpha()

    def get_player_mask(self) -> None:
        """Get mask of player sprite and draw to surface

        Returns:
            (pygame.mask): mask image of player
        """
        return mask.from_surface(self.image)

    def draw(self, surface, flipped:bool=False, player_mask:bool=False) -> None:
        """Draws player on surface

        Args:
            surface (pygame.surface): Surface object
        """
        self.change_sprite_number(self.sprite_number)
        if flipped:
            self.image = transform.flip(self.image,1,0)
        if player_mask:
            surface.blit(self.get_player_mask().to_surface(), self.position)
        else:
            surface.blit(self.image, self.position)
