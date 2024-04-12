import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
import streamlit as st




def predict_image(input_image):
    image = input_image.resize((28, 28))
    model = tf.keras.models.load_model("mnist_model.h5")
    if image.mode == 'RGBA':
        white_canvas = Image.new('RGB', image.size, '#aaa')
        white_canvas.paste(image, mask=image.split()[3])
        image = white_canvas
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Classifying...")

    image = image.convert('L')
    image = ImageOps.invert(image)
    img_inv = image.resize((28, 28))
    image_array = np.array(img_inv) / 255.0
    image_array = image_array.reshape((1, 28, 28, 1))

    my_prediction = model.predict(image_array)
    predicted_class = np.argmax(my_prediction, axis=1)
    return predicted_class


if __name__ == '__main__':
    st.title("Digit Guess App")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        prediction = predict_image(img)
        st.write(f"The machine think this number is {prediction}")
        st.image(img, caption="Uploaded Image", use_column_width=True)