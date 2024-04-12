import tensorflow as tf
from matplotlib import pyplot

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    minst = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = minst.load_data()
    pyplot.imshow(x_train[188, :, :], cmap="gray_r")
    pyplot.show()
    x_train = x_train/255
    x_test = x_test/255
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax'),
        ]
    )
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    #model.fit(x_train, y_train, epochs=10, validation_split=0.2)
    model.fit(x_train, y_train, epochs=5,  validation_split=0.2)
    # Evaluate the model on test data
    test_loss, test_acc = model.evaluate(x_test, y_test)
    model.save("class_model.keras")
    print("Test Accuracy:", test_acc)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
