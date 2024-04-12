import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import requests
from io import BytesIO

# Load the trained model
model = load_model("final_model.h5")

# Function to preprocess the image
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((28, 28))  # Resize to 28x28
    img.show()
    img_array = np.array(img)  # Convert to numpy array
    img_array = img_array.reshape(1, 28, 28, 1)  # Reshape to match model input shape
    img_array = img_array.astype('float32') / 255.0  # Normalize pixel values
    return img_array

# Function to classify the image
def classify_image(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)
    return predicted_class

# Function to allow user to upload an image and classify it
def classify_uploaded_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.show()
    predicted_class = classify_image(img)
    return predicted_class

# Main function
if __name__ == "__main__":
    print("Welcome to the Handwritten Digit Classifier!")
    print("Enter 'exit' to quit.")

    while True:
        user_input = input("Enter 'file' to classify an image from a file or 'url' to classify an image from a URL: ")

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'file':
            file_path = input("Enter the file path of the image: ")
            try:
                predicted_class = classify_image(file_path)
                print("Predicted Digit:", predicted_class)
            except Exception as e:
                print("Error:", e)
        elif user_input.lower() == 'url':
            image_url = input("Enter the URL of the image: ")
            try:
                predicted_class = classify_uploaded_image(image_url)
                print("Predicted Digit:", predicted_class)
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid input. Please enter 'file' or 'url'.")