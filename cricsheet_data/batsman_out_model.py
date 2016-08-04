"""
this is a model based on rnn and sentiment analysis

modelling between if over info gives information that
the batsman is out or not
"""

from __future__ import print_function
import random
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb

max_features = 20000
# cut texts after this number of words (among top max_features most common words)
maxlen = 7
batch_size = 32


def loading_data():
    X_train = np.loadtxt("data.out")
    print('X_train shape:', X_train.shape)
    print(X_train[0])

    X_test = np.loadtxt("data_test.out")
    print("X_test shape: ", X_test.shape)
    print(X_test[0])

    y_train = np.loadtxt("y_data.out")
    y_train = y_train.astype(int)
    print("y_train shape: ", y_train.shape)
    print(y_train[0:15])


    y_test = np.loadtxt("y_data_test.out")
    y_test = y_test.astype(int)
    print("y_test shape: ", y_test.shape)
    print(y_test[0:15])

    return (X_train, y_train, X_test, y_test)


def main():
    print('Loading data...')
    X_train, y_train, X_test, y_test = loading_data()

    print('Build model...')
    model = Sequential()
    model.add(Embedding(max_features, 128, input_length=maxlen, dropout=0.2))
    model.add(LSTM(128, dropout_W=0.2, dropout_U=0.2))  # try using a GRU instead, for fun
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    # try using different optimizers and different optimizer configs
    model.compile(loss='binary_crossentropy',
                            optimizer='adam',
                            metrics=['accuracy'])

    print('Train...')
    print(X_train.shape)
    print(y_train.shape)
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=15,
                    validation_data=(X_test, y_test))
    score, acc = model.evaluate(X_test, y_test,
                            batch_size=batch_size)

    print("")
    print('Test score:', score)
    print('Test accuracy:', acc)

    # save model as yaml file
    # save as json
    # save the architesture
    json_string = model.to_json()
    open('batsman_out_model.json', 'w').write(json_string)

    model.save_weights('batsman_out_model_weights.hdf5')

if __name__ == "__main__":
    main()
