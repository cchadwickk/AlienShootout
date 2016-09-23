import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #Class to represent aliens
    
    def __init__(self, settuns, screen):
        #Initialize the alien and set starting position
        super(Alien, self).__init__()
        self.screen = screen
        self.settuns = settuns
        
        #Load alien image
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        
        #Start each new alien near top left of screen
        #leaving space = width to its left and heigth above it
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #For calculations in future (see game_functions.create_fleet())
        self.x = float(self.rect.x)
        
    def blitme(self):
        #Draw self alien at specified location
        self.screen.blit(self.image, self.rect)
                
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
            
    def update(self):
        #Move alien to the right
        self.x += (self.settuns.alien_speed_factor * 
            self.settuns.fleet_direction)
        self.rect.x = self.x

            
            
