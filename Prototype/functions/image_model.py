
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
import numpy as np
import os

# Ensure TensorFlow version compatibility
# print("TensorFlow version:", tf.__version__)

# Define function to make prediction
def predict_image(img):
    print("TensorFlow version:", tf.__version__)
    model = tf.keras.models.load_model('Prototype/functions/EfficeintNet.h5')
    image = img.resize((32, 32))
    processed_img = keras.utils.img_to_array(image)
    processed_img = np.expand_dims(processed_img, axis=0)
    prediction = model.predict(processed_img)
    # decoded_predictions = decode_predictions(prediction, top=3)[0]
    return round(prediction[0][0])  # Assuming binary classification, get the first (and only) prediction
