import sys
import pygame

def check_events(stats, startbutton, addbutton, reducebutton):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_start_button(stats, startbutton, mouse_x, mouse_y)
            check_add_button(stats, addbutton, mouse_x, mouse_y)
            check_reduce_button(stats, reducebutton, mouse_x, mouse_y)


def check_start_button(stats, startbutton, mouse_x, mouse_y):
    if startbutton.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True

def check_add_button(stats, addbutton, mouse_x, mouse_y):
    if addbutton.rect.collidepoint(mouse_x, mouse_y) and stats.width<20:
        stats.width += 1
        stats.height += 1

def check_reduce_button(stats, reducebutton, mouse_x, mouse_y):
    if reducebutton.rect.collidepoint(mouse_x, mouse_y) and stats.width>3:
        stats.width -= 1
        stats.height -= 1
