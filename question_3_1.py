import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

model = tf.keras.models.load_model("final_model.h5")
file = input("enter image path")
img = cv2.imread(file)[:, :, 0]
img = np.invert(np.array([img]))
prediction = model.predict(img)
plt.imshow(img, cmap=plt.cm.binary)
plt.show
print(f"this is number we guessed: {np.argmax(prediction)}")