import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras import regularizers
import copy

class CNNModel:
    def __init__(self, trainset_address, gameStatus, board, robot_turn):
        self.trainset_address = trainset_address
        self.gameStatus = gameStatus
        self.board = board
        self.robot_turn = robot_turn
        self.model = Sequential()
        self.model.add(Conv2D(64, (3, 3), activation='relu', strides=(1, 1), input_shape=(self.board.width * 2, self.board.height * 2, 1)))
        self.model.add(Flatten())
        self.model.add(Dense(1, activation="tanh", kernel_regularizer=regularizers.l2(0.0001)))
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='mean_squared_error', optimizer=sgd,metrics=['accuracy','mae'])

    def train(self):
        boardrecord = []
        boardsets = []
        scores = []
        with open(self.trainset_address) as fin:
            for line in fin:
                blocks = line.replace("\n","").split("  ")
                if len(blocks) != 1:
                    blocks = [[float(b)] for b in blocks[:-1]]
                    boardrecord.append(blocks)
                else:
                    boardsets.append(boardrecord)
                    boardrecord = []
                    score = int(blocks[0])
                    scores.append([score])
        x_train = np.array(boardsets)
        y_train = np.array(scores)
        self.model.fit(x_train, y_train,batch_size=32,epochs=10)


    def predict(self):
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
        test_board = []
        for i in range(len(new_gameStatus)):
            test_board.append([[t] for t in new_gameStatus[i]])
        s = self.model.predict(np.array([test_board]))
        return s
