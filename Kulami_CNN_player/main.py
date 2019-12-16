import pygame
from settings import Settings
from marble import Marble
from start_button import StartButton
from reduce_button import ReduceButton
from add_button import AddButton
from input_filed import InputFiled
from board import Board
import game_functions as gf
import board_function as bf
import result_function as rf
from result import Result
from restart_button import RestartButton
from robot import Robot
from status import Status
from CNN_model import CNNModel


class Stats:
    def __init__(self):
        self.width = 6
        self.height = 6
        self.game_active = False
        self.game_restart = False


def run_game():
    pygame.init()
    Kulami_settings = Settings()
    background = pygame.image.load(Kulami_settings.initial_background)
    pygame.display.set_caption("Kulami")
    while True:
        screen = pygame.display.set_mode((background.get_width(), background.get_height()))
        screen.blit(background, (0, 0))
        startbutton = StartButton(screen)
        startbutton.blitme()
        addbutton = AddButton(screen, startbutton)
        addbutton.blitme()
        reducebutton = ReduceButton(screen, startbutton)
        reducebutton.blitme()
        inputfield = InputFiled(screen, addbutton, reducebutton)
        inputfield.blitme()
        stats = Stats()
        font = pygame.font.Font(Kulami_settings.font, 40)
        surface = font.render(str(stats.width), True, Kulami_settings.font_color)
        screen_rect = screen.get_rect()
        screen.blit(surface, (
            int(screen_rect.centerx - 0.5 * surface.get_width()),
            int(reducebutton.rect.centery - 0.5 * surface.get_height())))

        while True:
            gf.check_events(stats, startbutton, addbutton, reducebutton)
            # marble.blitme_xy(0,0)
            inputfield.blitme()
            surface = font.render(str(stats.width), True, (154, 202, 64))
            screen.blit(surface, (int(screen_rect.centerx - 0.5 * surface.get_width()),
                                  int(reducebutton.rect.centery - 0.5 * surface.get_height())))
            pygame.display.flip()
            if stats.game_active:
                break
        screen = pygame.display.set_mode((stats.width * Kulami_settings.hole_size, stats.height * Kulami_settings.hole_size))
        board = Board(screen, stats.width, stats.height, Kulami_settings.bg_color, Kulami_settings.hole_size, Kulami_settings.tile_edge_color)
        board.blitme()
        pygame.display.flip()
        gameStatus = Status(stats.width, stats.height)
        board.init_board_feature()
        cnnModel = CNNModel(Kulami_settings.trainset_address+"_size_"+str(board.width)+".txt", gameStatus, board, Kulami_settings.robot_turn)
        cnnModel.train()
        robot = Robot(gameStatus, board, screen, Kulami_settings.hole_size, "Minmax", Kulami_settings.robot_turn, Kulami_settings.robot_IQ, cnnModel)
        while True:
            if gameStatus.turn == Kulami_settings.robot_turn:
                robot.play()
                continue
            g = bf.check_events(gameStatus, screen, Kulami_settings.hole_size, board)

            pygame.display.flip()
            if gameStatus.end:
                print("Game over")
                print("red score:", gameStatus.red_score, "black score:", gameStatus.black_score)
                if gameStatus.red_score > gameStatus.black_score:
                    print("RED WIN!")
                    gameStatus.result = 0
                elif gameStatus.black_score > gameStatus.red_score:
                    print("BLACK WIN!")
                    gameStatus.result = 1
                else:
                    print("TIE!")
                    gameStatus.result = 2
                break
        result = Result(screen, Kulami_settings.bg_color, gameStatus, Kulami_settings)
        result.blitme()
        restartbutton = RestartButton(screen)
        restartbutton.blitme()
        pygame.display.flip()
        while True:
            g = rf.check_events(stats, restartbutton)
            if stats.game_restart:
                stats.game_restart = False
                break


run_game()
