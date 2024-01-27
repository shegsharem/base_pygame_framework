"""Python 3.12.1"""
from pygame import sprite, Vector2, transform, image, Surface, key, quit
from pygame.locals import *

class Player(sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)

        self.sprite_number = 0
        self.touching_ground = False

        # Build sprite list: #############################################################
        # {Sprite Number: (Image, Rect)}
        self.player_sprites = {}

        for i in range(6):
            img = transform.scale_by(
                image.load('assets/images/player/player'+str(i)+'.png').convert_alpha(),2)
            self.player_sprites[i] = img, img.get_rect()
        ###################################################################################

        self.image = self.player_sprites[self.sprite_number][0]
        self.rect = self.player_sprites[self.sprite_number][1]
        self.old_rect = None

        self.position = Vector2(0,0)
        self.direction = Vector2()
        self.speed = 200


    def input(self) -> None:
        """Get keyboard input"""
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            quit()
            exit()

        if keys[K_w]:
            self.direction.y = -1
            self.speed += 1
        elif keys[K_s]:
            self.direction.y = 1
        else: self.direction.y = 1

        if keys[K_d]:
            self.direction.x = 1
        elif keys[K_a]:
            self.direction.x = -1
        else: self.direction.x = 0

    def collision(self,axis:str,group:sprite.Group) -> None:
        """Checks if player is colliding with sprite group

        :param axis: axis to check `(x or y)`
        :type axis: str
        :param group: collideable sprite group
        :type group: sprite.Group
        """
        collisions = sprite.spritecollide(self,group,False)
        if collisions:
            # Check x direction
            if axis == "x":
                for s in collisions:
                    if self.rect.right >= s.rect.left and self.old_rect.right <= s.rect.left:
                        self.rect.right = s.rect.left
                        self.position.x = self.rect.x
                    if self.rect.left <= s.rect.right and self.old_rect.left >= s.rect.right:
                        self.rect.left = s.rect.right
                        self.position.x = self.rect.x

            # Check y direction
            if axis == "y":
                for s in collisions:
                    if self.rect.top <= s.rect.bottom and self.old_rect.top >= s.rect.bottom:
                        self.rect.top = s.rect.bottom
                        self.position.y = self.rect.y
                    if self.rect.bottom >= s.rect.top and self.old_rect.bottom <= s.rect.top:
                        self.rect.bottom = s.rect.top
                        self.position.y = self.rect.y
                        self.touching_ground = True

    def update(self, deltatime:float, group:sprite.Group) -> None:
        """Rectangle update method 

        :param deltatime: used for smooth motion
        :type deltatime: float
        """
        if self.touching_ground:
            self.sprite_number = 3
            self.image = self.player_sprites[self.sprite_number][0]
            self.rect = self.player_sprites[self.sprite_number][1]

        self.old_rect = self.rect.copy()
        self.input()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal Collision
        self.position.x += (self.direction.x*self.speed*deltatime)
        self.rect.x = round(self.position.x)
        self.collision("x", group)

        # Vertical Collision
        self.position.y += (self.direction.y*self.speed*deltatime)
        self.rect.y = round(self.position.y)
        self.collision("y", group)

        
