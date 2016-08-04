from keras.models import model_from_json

from batsman_out_model import loading_data, \
                            batch_size


def main():
    print('Loading data...')
    X_train, y_train, X_test, y_test = loading_data()

    print("loading the model")
    model = model_from_json(open('batsman_out_model.json').read())

    print("loading the previous weights")
    model.load_weights('batsman_out_model_weights.hdf5')

    # Finally, before it can be used, the model shall be compiled.
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

    print("saving model and weights")
    json_string = model.to_json()
    open('batsman_out_model_new.json', 'w').write(json_string)

    model.save_weights('batsman_out_model_weights_new.hdf5')

    print("Done")

if __name__ == "__main__":
    main()
