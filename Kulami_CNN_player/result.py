import pygame

class Result():
    def __init__(self, screen, boardcolor, gameStatus, setting):
        self.boardcolor = boardcolor
        self.screen = screen
        self.gameStatus = gameStatus
        self.setting = setting

    def blitme(self):
        rect = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA, 32)
        rect.fill((self.boardcolor[0], self.boardcolor[1], self.boardcolor[2], 220))
        self.screen.blit(rect, (0, 0))
        if self.gameStatus.result == 0:
            slogan = "RED WIN!"
        elif self.gameStatus.result == 1:
            slogan = "BLACK WIN!"
        else:
            slogan = "TIE!"
        font = pygame.font.Font(self.setting.font, int(self.screen.get_width()/len(slogan)))
        surface = font.render(slogan, True, self.setting.font_color)
        self.screen.blit(surface, (int(self.screen.get_width()/2 - 0.5 * surface.get_width()),
                              int(self.screen.get_height())/3 - 0.5 * surface.get_height()))





