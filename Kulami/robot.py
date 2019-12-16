import random as rd
import board_function as bf
from marble import Marble
import copy


class Robot:
    def __init__(self, gameStatus, board, screen, hole_size, intelligence, robot_turn, deep):
        self.gameStatus = gameStatus
        self.board = board
        self.screen = screen
        self.hole_size = hole_size
        self.intelligence = intelligence
        self.robot_turn = robot_turn
        self.deep = deep


    def get_potential_position(self):
        potential_position = []
        if self.gameStatus.last_opponent[0] == -1 and self.gameStatus.last_opponent[1] == -1:
            for i in range(self.gameStatus.width):
                for t in range(self.gameStatus.height):
                    potential_position.append((i, t))
        else:
            x = self.gameStatus.last_opponent[0]
            y = self.gameStatus.last_opponent[1]
            for i in range(self.gameStatus.width):
                if bf.check_avaliable(self.gameStatus, i, y, self.board, False):
                    potential_position.append((i, y))
            for i in range(self.gameStatus.height):
                if bf.check_avaliable(self.gameStatus, x, i, self.board, False):
                    potential_position.append((x, i))
        return potential_position

    def decision_randomly(self, potential_position):
        print(potential_position)
        decision = rd.choice(potential_position)
        return decision

    def decision_minmax(self, potential_position, deep):
        if len(potential_position) == 0 or deep <= 0:
            if self.robot_turn == 0:
                return (self.gameStatus.last_opponent, self.gameStatus.red_score - self.gameStatus.black_score)
            else:
                return (self.gameStatus.last_opponent, self.gameStatus.black_score - self.gameStatus.red_score)
        gameStatus_backup = copy.deepcopy(self.gameStatus)
        results = []
        for candidate in potential_position:
            x = candidate[0]
            y = candidate[1]
            if bf.check_avaliable(self.gameStatus, x, y, self.board, True):
                self.gameStatus.available[x][y] = 1
                self.gameStatus.occupy[x][y] = self.gameStatus.turn
                if self.gameStatus.turn == 1:
                    self.gameStatus.turn = 0
                else:
                    self.gameStatus.turn = 1
                self.gameStatus.last_opponent = (x, y)
                # calculate score
                bf.calculate_score(self.gameStatus, self.board)
                new_potential_position = self.get_potential_position()
                results.append((candidate, self.decision_minmax(new_potential_position, deep-1)[1]))
                self.gameStatus.recover(gameStatus_backup)
        decision = results[0]
        if self.gameStatus.turn == self.robot_turn:  # max the difference
            for r in results:
                if decision[1] < r[1]:
                    decision = r
        else:  # mini the difference
            for r in results:
                if decision[1] > r[1]:
                    decision = r
        return decision

    def put_marble(self, x, y):
        if bf.check_avaliable(self.gameStatus, x, y, self.board, True):
            # mention that available table is not match true board, it is diagonally flipped
            self.gameStatus.available[x][y] = 1
            self.gameStatus.occupy[x][y] = self.gameStatus.turn
            marble = Marble(self.screen, self.gameStatus)
            marble.blitme_xy(int((x + 0.5) * self.hole_size), int((y + 0.5) * self.hole_size))
            if self.gameStatus.turn == 1:
                self.gameStatus.turn = 0
            else:
                self.gameStatus.turn = 1
            self.gameStatus.last_opponent = (x, y)
            # calculate score
            bf.calculate_score(self.gameStatus, self.board)
            print("red score:", self.gameStatus.red_score, "black score:", self.gameStatus.black_score)
            # check game end
            if bf.check_end(self.gameStatus, self.board, x, y):
                self.gameStatus.end = True

    def play(self):
        potential_position = self.get_potential_position()
        # print(potential_position)
        if self.intelligence == "Random":
            decision = self.decision_randomly(potential_position)
        if self.intelligence == "Minmax":
            decision = self.decision_minmax(potential_position, self.deep)[0]
        self.put_marble(decision[0], decision[1])
