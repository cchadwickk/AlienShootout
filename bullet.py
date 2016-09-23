import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #Class for bullets
    
    def __init__(self, settuns, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(
            0, 0, settuns.bullet_width, settuns.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #Store bullets position in decimal
        self.y = float(self.rect.top)
        self.color = settuns.bullet_color
        self.speed_factor = settuns.bullet_speed_factor
    
    def update(self):
        #For movement of bullets
        self.y -= self.speed_factor #Float movement variable
        #Transfer to actual variable
        self.rect.y = self.y
        
    def draw_bullet(self):
        #Actually draw the bullet on screen
        pygame.draw.rect(self.screen, self.color, self.rect)
        
