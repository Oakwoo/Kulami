import pygame

class ReduceButton():
    def __init__(self, screen, startbutton):
        self.screen = screen
        self.image = pygame.image.load('image/reduce_button.png')
        self.image = pygame.transform.scale(self.image, (int(screen.get_height()*0.075), int(screen.get_height()*0.075)))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.left = startbutton.rect.left
        self.rect.centery = int(screen.get_height()*0.82)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def blitme_xy(self, x, y):
        self.screen.blit(self.image, (x, y))
