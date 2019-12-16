import pygame

class Marble():
    def __init__(self, screen, gameStatus):
        self.screen = screen
        if gameStatus.turn == 0:
            self.image = pygame.image.load('image/red_marble.png')
        else:
            self.image = pygame.image.load('image/black_marble.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

    def blitme_xy(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        self.screen.blit(self.image, self.rect)
