import sys
import pygame
from marble import Marble
import math


def check_events(gameStatus, screen, hole_size, board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x = math.floor(mouse_x / hole_size)
            y = math.floor(mouse_y / hole_size)
            if check_avaliable(gameStatus, x, y, board, True):
                # mention that available table is not match true board, it is diagonally flipped
                gameStatus.available[x][y] = 1
                gameStatus.occupy[x][y] = gameStatus.turn
                marble = Marble(screen, gameStatus)
                marble.blitme_xy(int((x + 0.5) * hole_size), int((y + 0.5) * hole_size))
                if gameStatus.turn == 1:
                    gameStatus.turn = 0
                else:
                    gameStatus.turn = 1
                gameStatus.last_opponent = (x, y)
                # calculate score
                calculate_score(gameStatus, board)
                print("red score:", gameStatus.red_score, "black score:", gameStatus.black_score)
                # check game end
                if check_end(gameStatus, board, x, y):
                    gameStatus.end = True


def check_avaliable(gameStatus, x, y, board, indeed):
    tile = -1
    for i, t in enumerate(board.tiles):
        if x >= t[0] and y >= t[1] and x < t[0] + t[2] and y < t[1] + t[3]:
            tile = i
            break
    if gameStatus.available[x][y] == 1:
        if indeed: print("This position has been occupied!")
        return False
    if gameStatus.last_opponent[0] != -1 and gameStatus.last_opponent[1] != -1 and x != gameStatus.last_opponent[
        0] and y != gameStatus.last_opponent[1]:
        if indeed: print(
            "The marble must be placed either horizontally or vertically in relation to the marble the opponent has just played!")
        return False
    if gameStatus.tile_opponent != -1 and tile == gameStatus.tile_opponent:
        if indeed: print(
            "The marble cannot be placed on the same tile on which the opponent has just played their marble.")
        return False
    if gameStatus.tile_self != -1 and tile == gameStatus.tile_self:
        if indeed: print("The marble cannot be placed on the same tile where the player placed their previous marble. ")
        return False
    if indeed:
        gameStatus.tile_self = gameStatus.tile_opponent
        gameStatus.tile_opponent = tile
    return True


def calculate_score(gameStatus, board):
    red_score = 0
    black_score = 0
    for t in board.tiles:
        red_count = 0
        black_count = 0
        for x in range(t[0], t[0] + t[2]):
            for y in range(t[1], t[1] + t[3]):
                if gameStatus.occupy[x][y] == 0:
                    red_count += 1
                if gameStatus.occupy[x][y] == 1:
                    black_count += 1
        if black_count > red_count:
            black_score += t[2] * t[3]
        if red_count > black_count:
            red_score += t[2] * t[3]
    gameStatus.red_score = red_score
    gameStatus.black_score = black_score
    #print("red score:", gameStatus.red_score, "black score:", gameStatus.black_score)


def check_end(gameStatus, board, x, y):
    for i in range(gameStatus.width):
        if check_avaliable(gameStatus, i, y, board, False):
            return False
    for i in range(gameStatus.height):
        if check_avaliable(gameStatus, x, i, board, False):
            return False
    return True
