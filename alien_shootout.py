import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    settuns = Settings()
    screen = pygame.display.set_mode(
        (settuns.scr_width, settuns.scr_height))
    pygame.display.set_caption("Alien Shootout")
    
    play_button = Button(settuns, screen, "Play")
    stats = GameStats(settuns)
    sb = Scoreboard(settuns, screen, stats)
    ship = Ship(screen, settuns)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(settuns, screen, ship, aliens)
    
    #Start the main loop for the game.
    while True:
        gf.check_events(settuns, screen, stats, sb, play_button, ship, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settuns, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(settuns, stats, screen, sb, ship, aliens, bullets)
        gf.update_screen(settuns, screen, stats, sb, ship, aliens, bullets, play_button)
        
run_game()
