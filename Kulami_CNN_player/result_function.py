import sys
import pygame

def check_events(stats, restartbutton):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_restart_button(stats, restartbutton, mouse_x, mouse_y)

def check_restart_button(stats, restartbutton, mouse_x, mouse_y):
    if restartbutton.rect.collidepoint(mouse_x, mouse_y):
        stats.game_restart = True