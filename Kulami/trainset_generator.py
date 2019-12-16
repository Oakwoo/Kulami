import copy
class TrainsetGenerator:
        def __init__(self, gameStatus, board, trainset_address, robot_turn):
            self.gameStatus = gameStatus
            self.board = board
            self.trainset_address = trainset_address
            self.gameStatusRecord = []
            self.score = 0
            self.robot_turn = robot_turn

        def recordStatus(self):
            new_gameStatus = copy.deepcopy(self.board.board_feature)
            for x in range(self.gameStatus.width):
                for y in range(self.gameStatus.height):
                    if self.gameStatus.occupy[x][y] == -1:
                        continue
                    else:
                        tile = -1
                        normalize_score = 1
                        for i, t in enumerate(self.board.tiles):
                            if x >= t[0] and y >= t[1] and x < t[0] + t[2] and y < t[1] + t[3]:
                                tile = i
                                normalize_score = 1/(t[2] * t[3])
                                break
                        if self.gameStatus.occupy[x][y] == self.robot_turn:
                            new_gameStatus[2 * x][2 * y] = normalize_score
                        else:
                            new_gameStatus[2 * x][2 * y] = -1 * normalize_score
            self.gameStatusRecord.append(new_gameStatus)

        def write(self, score):
            with open(self.trainset_address,'a') as fout:
                for gameStatus in self.gameStatusRecord:
                    for i in range(len(gameStatus)):
                        for t in range(len(gameStatus[0])):
                            fout.write(str(gameStatus[i][t])+"  ")
                        fout.write("\n")
                    fout.write(str(score) + "\n")
