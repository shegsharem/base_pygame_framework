"""PLayer module"""
from typing import Any
from pygame import sprite, image, error, transform

DEFAULT_SPRITE_DIR = 'assets/images/player/player'


class Player:
    """Player class"""
    def __init__(self, filepath:str=DEFAULT_SPRITE_DIR) -> None:
        """Load the sprites, all images should be the same size."""
        super().__init__()
        self.image - 

    def flip(self):


player = Player()
player.update

class chungus(pygame.sprite.Sprite):#
    """Player class"""
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.transform.scale_by(
            pygame.image.load('assets/images/circle.png').convert_alpha(),
            factor=4
        )

        self.velocity = pygame.Vector2(0,0)
        self.position = pygame.Vector2(0,0)

        self.rect = self.image.get_rect()
        self.outline = get_mask_outline(self.image, (1,1))
        self.outline_rect = self.outline.get_rect()

        # Player flags #############
        self.touching_ground = False
        self.double_jump = True
        self.moving_right = False
        self.moving_left = False
        self.moving_x = False
        ############################

        # Constants ######
        self.gravity = 3
        self.jump_speed = -600
        self.friction = 3
        self.movement_speed = 400
        ##################

    def jump(self) -> None:
        """Make player jump"""
        if self.touching_ground:
            self.velocity.y = self.jump_speed
            self.double_jump = True
        
        elif not self.touching_ground and self.double_jump:
            self.velocity.y = self.jump_speed
            self.double_jump = False

    def left(self) -> None:
        """Move player left"""
        self.velocity.x = -self.movement_speed
        self.moving_x = True

    def right(self) -> None:
        """Move player right"""
        self.velocity.x = self.movement_speed
        self.moving_x = True

    def move(self, position:pygame.Vector2,
              velocity:pygame.Vector2) -> pygame.Vector2:
        """Change player position by a given velocity (pixels)"""
        return position + velocity

    def update(self,surface:pygame.Surface,
        dt:float,level:pygame.sprite.Group=None) -> None:
        """Update player position and draw on surface.
        Tries rendering next frame and corrects for collisions.
        Args:
            dt (float): time difference between frames (ms/frame)
        """

        # Collisions ################################################################
        collision_list = []
        collision_types = {'top': False,'bottom': False,'right': False,'left': False}

        self.position += (self.velocity)
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

        for sprite in level:
            if self.rect.colliderect(sprite.rect):
                collision_list.append(sprite.rect)

        # Check y direction collisions #############
        for sprite_rect in collision_list:
            if self.velocity.y >= 0:
                self.rect.bottom = sprite_rect.top
                collision_types['bottom'] = True

            elif self.velocity.y < 0:
                self.rect.top = sprite_rect.bottom
                collision_types['top'] = True

        # Check x direction collisions #############
            elif self.velocity.x > 0:
                #self.rect.right = sprite_rect.left
                collision_types['right'] = True

            elif self.velocity.x < 0:
                #self.rect.left = sprite_rect.right
                collision_types['left'] = True
        ################################################################################

        print(collision_types)

        if collision_types['left']:
            self.velocity.x = 0
        
        if collision_types['right']:
            self.velocity.x = 0

        if collision_types['bottom']:
            self.touching_ground = True
            self.velocity.y =0
            if collision_types['right']:
                self.velocity.x = 0
        
        if not collision_types['bottom']:
            self.touching_ground = False
            self.velocity.y += (self.gravity)


        #Friction
        if self.touching_ground:
            if self.velocity.x // 1:
                if abs(self.velocity.x) < self.friction:
                    self.velocity.x = 0
                elif self.velocity.x > 0:
                    self.moving_right = True
                    self.velocity.x -= self.friction
                elif self.velocity.x < 0:
                    self.moving_left = True
                    self.velocity.x += self.friction


        pygame.draw.rect(surface, (200,200,200), self.outline_rect)
        surface.blit(self.image, self.rect)