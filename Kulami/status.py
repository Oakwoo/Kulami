import copy
class Status:
    def __init__(self, width, height):
        self.turn = 0
        self.width = width
        self.height = height
        self.available = [[0 for t in range(height)] for i in range(width)]
        self.occupy = [[-1 for t in range(height)] for i in range(width)]
        self.last_opponent = (-1, -1)
        self.tile_opponent = -1
        self.tile_self = -1
        self.end = False
        self.red_score = 0
        self.black_score = 0
        self.result = -1

    def recover(self, gameStatus_backup):
        self.turn = gameStatus_backup.turn
        self.width = gameStatus_backup.width
        self.height = gameStatus_backup.height
        self.available = copy.deepcopy(gameStatus_backup.available)
        self.occupy = copy.deepcopy(gameStatus_backup.occupy)
        self.last_opponent = gameStatus_backup.last_opponent
        self.tile_opponent = gameStatus_backup.tile_opponent
        self.tile_self = gameStatus_backup.tile_self
        self.end = gameStatus_backup.end
        self.red_score = gameStatus_backup.red_score
        self.black_score = gameStatus_backup.black_score
        self.result = gameStatus_backup.result
