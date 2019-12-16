import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras import regularizers
#这一行新加的，用于导入绘图包
from keras.utils import plot_model
'''in_x = network = Input((4, self.board_width, self.board_height)) #dimensions with number of elements in the dimensions

network = Conv2D(32, (3, 3), padding="same", data_format="channels_first", activation="relu", kernel_regularizer=l2(1e-4))(network)
network = Conv2D(64, (3, 3), padding="same", data_format="channels_first", activation="relu", kernel_regularizer=l2(1e-4))(network)
network = Conv2D(128, (3, 3), padding="same", data_format="channels_first", activation="relu", kernel_regularizer=l2(1e-4))(network)

policy_net = Conv2D(4, (1, 1), data_format="channels_first", activation="relu", kernel_regularizer=l2(1e-4))(network)
policy_net = Flatten()(policy_net)
policy_net = Dense(board_width*board_height, activation="softmax", kernel_regularizer=l2(1e-4))(policy_net)

value_net = Conv2D(2, (1, 1), data_format="channels_first", activation="relu", kernel_regularizer=l2(1e-4))(network)
value_net = Flatten()(value_net)
value_net = Dense(64, kernel_regularizer=l2(1e-4))(value_net)
value_net = Dense(1, activation="tanh", kernel_regularizer=l2(0.0001))(value_net)

model = Model(in_x, [policy_net, value_net])

model.compile(optimizer="adam", loss=['categorical_crossentropy', 'mean_squared_error'])'''

boardrecord = []
boardsets = []
scores = []
with open("trainset_size_6.txt") as fin:
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
x_train = np.array(boardsets[:int(0.9*len(boardsets))])
y_train = np.array(scores[:int(0.9*len(scores))])
x_test = np.array(boardsets[int(0.9*len(boardsets)):])
y_test = np.array(scores[int(0.9*len(scores)):])

model = Sequential()
#一层卷积层，包含了32个卷积核，大小为3*3
model.add(Conv2D(64, (3, 3), activation='relu', strides=(1, 1), input_shape=(12, 12, 1)))
'''#一个最大池化层，池化大小为2*2
model.add(MaxPooling2D(pool_size=(2, 2)))
#遗忘层，遗忘速率为0.25
model.add(Dropout(0.25))
#添加一个卷积层，包含64个卷积和，每个卷积和仍为3*3
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
#来一个池化层
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
#压平层
model.add(Flatten())
#来一个全连接层
model.add(Dense(256, activation='relu'))
#来一个遗忘层
model.add(Dropout(0.5))
#最后为分类层
model.add(Dense(10, activation='softmax'))'''
model.add(Flatten())
model.add(Dense(1, activation="tanh", kernel_regularizer=regularizers.l2(0.0001)))


sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error', optimizer=sgd,metrics=['accuracy','mae'])

model.fit(x_train, y_train,batch_size=32,epochs=10)
s = model.predict(np.array([x_test[0]]))
print(y_test[0])
print(s)
