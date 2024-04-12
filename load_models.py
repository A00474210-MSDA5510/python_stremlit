import numpy as np
from PIL import Image
import tensorflow as tf
import streamlit as st


def classify_image_RGBA(img):
    splited_img_list = img.split()
    converted_list = [i.convert("L") for i in splited_img_list]
    array_image = np.array(converted_list[-1])
    array_image = np.expand_dims(array_image, axis = 0) # Add a batch dimension
    # Check if all pixel values in the alpha channel are either 0 (fully transparent) or 255 (fully opaque)
    return array_image


def classify_image_RGB(img):
    array_image = np.array(img)[:, :, 0] / 255.0  # Normalize pixel values and select only the grayscale channel
    array_image = np.expand_dims(array_image, axis=0)  # Add a batch dimension
    return array_image

def predict_image(input_image):
    img = input_image.resize((28, 28))
    model = tf.keras.models.load_model("my_model.keras")
    img_to_predict = None
    if img.mode =="RBG":
        img_to_predict = classify_image_RGB(img)
    elif img.mode == "RGBA":
        alpha_channel = img.split()[-1]
        is_empty = all(pixel == 0 or pixel == 255 for pixel in alpha_channel.getdata(0))
        if is_empty:
            img_to_predict = classify_image_RGB(img)
        else:
            img_to_predict = classify_image_RGBA(img)
    prediction_result = model.predict(img_to_predict)
    return prediction_result


if __name__ == '__main__':
    st.title("Digit Guess App")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        prediction = predict_image(img)
        st.write(f"The machine think this number is {np.argmax(prediction)}")
        st.image(img, caption="Uploaded Image", use_column_width=True)