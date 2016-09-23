import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self, screen, settuns):
        super(Ship, self).__init__()
        self.screen = screen
        
        #Load ship image and get its rectangle
        self.image = pygame.image.load('Images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.settuns = settuns
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)
        
        #Movement flags
        self.moving_left = False
        self.moving_right = False
        
    def update(self):
        #Update the position based on flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settuns.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settuns.ship_speed_factor
            
        self.rect.centerx = self.center
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
