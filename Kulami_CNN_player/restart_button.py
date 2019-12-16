import pygame

class RestartButton():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('image/start_button.png')
        self.image = pygame.transform.scale(self.image, (int(screen.get_width()*0.4), int(screen.get_height()*0.2)))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = int(screen.get_height()*0.72)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def blitme_xy(self, x, y):
        self.screen.blit(self.image, (x, y))
