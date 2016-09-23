import pygame.font

class Button():
    
    def __init__(self, settuns, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        #Create font instance to render text onscreen(fontType, fontSize)
        self.font = pygame.font.SysFont(None, 48)
        
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        #True for antialiasing on or off.
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        #Fill to color the box, blit to draw the text image
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
