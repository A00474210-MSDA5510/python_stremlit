import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt


def load_data():
    # Load the MNIST dataset
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

    # Normalize the images to [0, 1] range
    train_images, test_images = train_images / 255.0, test_images / 255.0

    # Reshape the images to (28, 28, 1) to fit the model input
    train_images = train_images.reshape((-1, 28, 28, 1))
    test_images = test_images.reshape((-1, 28, 28, 1))

    return train_images, train_labels, test_images, test_labels


def build_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
    ])

    # Compile the model
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model


def plot_history(history):
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='validation accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(loc='lower right')
    plt.show()


def main():
    train_images, train_labels, test_images, test_labels = load_data()
    model = build_model()
    history = model.fit(train_images, train_labels, epochs=10,
                        validation_data=(test_images, test_labels))
    plot_history(history)
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    model.save("model_v2.keras")
    print(f"Test accuracy: {test_acc}")


if __name__ == "__main__":
    main()