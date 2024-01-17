"""Player module"""
import pygame

class Player1(pygame.sprite.Sprite):
    """New player class"""
    def __init__(self):
        super().__init__()
        self.velocity = [0,1]
        self.position = [3,3]

        __filepath = 'assets/images/circle.png'
        self.image = pygame.image.load(__filepath).convert_alpha()
        self.image = pygame.transform.scale_by(self.image,4)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.position[0], self.position[1])

        # Constants ######
        self.gravity = 2
        self.jump_speed = -600
        self.friction = 3
        self.movement_speed = 400
        ##################
    
    def move(self):
        self.rect = self.rect.move(self.velocity[0], self.velocity[1])
    
    def update(self, surface:pygame.Surface, level:pygame.sprite.Group):
        self.move()
        pygame.draw.line(surface,(0,0,0),(0,self.rect.top), (surface.get_width(),self.rect.top))
        surface.blit(self.image, self.rect)