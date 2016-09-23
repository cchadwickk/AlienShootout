import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
            
def check_keydown_events(event, settuns, screen, stats, sb, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settuns, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(settuns, stats, sb)
        
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(settuns, screen, stats, sb, play_button, ship, bullets):
    #Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type ==  pygame.KEYDOWN:
            check_keydown_events(
                event, settuns, screen, stats, sb, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                settuns, stats, sb, play_button, mouse_x, mouse_y)
    
def check_play_button(settuns, stats, sb, play_button, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(settuns, stats, sb)
        
def start_game(settuns, stats, sb):
    if not stats.game_active:
        settuns.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
def update_screen(all_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    #ORDERING OF BLOCKS HERE DECIDES LAYERING ON MAIN GAME SCREEN
    #Redraw the screen with background color 
    screen.fill(all_settings.bg_color)
    #Redraw all bullets, ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    #Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(settuns, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #groupcollide(1st grp, 2nd grp, rm 1st grp?, rm 2nd grp?)
    check_bullet_alien_collisions(settuns, screen, stats, sb, ship, aliens, bullets)
    
def check_bullet_alien_collisions(settuns, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settuns.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        stats.level += 1
        sb.prep_level()
        bullets.empty()
        settuns.increase_speed_and_score()
        create_fleet(settuns, screen, ship, aliens)
            
def fire_bullet(settuns, screen, ship, bullets):
    #Create bullet and add to the group
    if(len(bullets) < settuns.bullet_allowed):
        new_bullet = Bullet(settuns, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(settuns, alien_width):
    available_space_x = settuns.scr_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(settuns, ship_height, alien_height):
    available_space_y = (settuns.scr_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(settuns, screen, aliens, alien_number, row_number):
    alien = Alien(settuns, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(settuns, screen, ship, aliens):
    #Create alien and find number of aliens in a row.
    #Spacing between each alien is equal to one alien width.
    alien = Alien(settuns, screen)
    number_aliens_x = get_number_aliens_x(settuns, alien.rect.width)
    number_rows = get_number_rows(settuns, ship.rect.height, alien.rect.height)
    
    #Create first row of aliens
    for row_number in range(number_rows):
       for alien_number in range(number_aliens_x):
            create_alien(settuns, screen, aliens, alien_number, row_number)

def check_fleet_edges(settuns, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settuns, aliens)
            break
            
def change_fleet_direction(settuns, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settuns.fleet_drop_speed
    settuns.fleet_direction *= -1

def update_aliens(settuns, stats, screen, sb, ship, aliens, bullets):
    check_fleet_edges(settuns, aliens)
    aliens.update()
    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settuns, stats, screen, sb, ship, aliens, bullets)
    check_aliens_bottom(settuns, stats, screen, sb, ship, aliens, bullets)

def ship_hit(settuns, stats, screen, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(settuns, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_variable(True)

def check_aliens_bottom(settuns, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settuns, stats, screen, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
