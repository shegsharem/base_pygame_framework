"""Python 3.12.1"""
from pygame import sprite, Vector2, transform, image
from src.collisions import intersecting_rect_with_sprite_group

class Player(sprite.Sprite):
    """Player Class"""
    def __init__(self, position:tuple=(0,0)) -> None:
        """Create player instance

        :param position: coordinate `(x,y)`, defaults to `(0,0)`
        :type position: tuple, optional
        """
        super().__init__()

        # Player Flags #############
        self.sprite_number = 0
        self.flipped = False
        self.touching_ground = False
        self.moving_left = False
        self.moving_right = True
        ############################

        # Player Variables #############################
        self.position = Vector2(position[0],position[1])
        self.velocity = Vector2(0,0)
        self.acceleration = Vector2(0,0)
        self.gravity = 1
        self.friction = 0.2
        self.terminal_velocity = 200
        ################################################

        # Build sprite list: #############################################################
        # {Sprite Number: (Image, Rect)}
        self.player_sprites = {}

        for i in range(6):
            img = transform.scale_by(
                image.load('assets/images/player/player'+str(i)+'.png').convert_alpha(),3)
            self.player_sprites[i] = img, img.get_bounding_rect()
        ###################################################################################

        self.image = self.player_sprites[self.sprite_number][0]
        self.rect = self.player_sprites[self.sprite_number][1]

    def move(self, deltatime:float) -> None:
        """Move player

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        # Gravity ############################
        #if not self.touching_ground:
        #    self.acceleration.y = self.gravity
        ######################################

        self.velocity += self.acceleration
        self.position += (self.velocity*deltatime)
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def update(self, deltatime:float) -> None:
        """Player update method

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        # Update player image ##############################################
        # Sprite number limiter
        if self.sprite_number > len(self.player_sprites)-1:
            self.sprite_number = len(self.player_sprites)-1
        elif self.sprite_number < 0:
            self.sprite_number = 0

        # Set player rect
        self.rect = self.player_sprites[self.sprite_number][1]

        if self.moving_left:
            if not self.flipped:
                self.image = transform.flip(
                    self.player_sprites[self.sprite_number][0],True, False)
                self.flipped = True

        if self.moving_right:
            if self.flipped:
                self.image = transform.flip(
                    self.player_sprites[self.sprite_number][0], True, False)
                self.flipped = False
            else:
                self.image = self.player_sprites[self.sprite_number][0]
        ####################################################################

        self.move(deltatime)
