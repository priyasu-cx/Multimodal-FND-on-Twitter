
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Ensure TensorFlow version compatibility
print("TensorFlow version:", tf.__version__)



# Define image preprocessing function
def preprocess_image(img):
    img = img.resize(( 32, 32))  # EfficientNetV2 typical input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Create batch axis
    img_array = img_array / 255.0  # Normalize to [0, 1]
    return img_array

# Define function to make prediction
def predict_image(img):
    print("TensorFlow version:", tf.__version__)
    model = tf.keras.models.load_model(r'D:\Final Year project\Multimodal-FND-on-Twitter\Prototype\functions\EfficientNet_model.h5')
    processed_img = preprocess_image(img)
    prediction = model.predict(processed_img)
    return prediction[0][0]  # Assuming binary classification, get the first (and only) prediction

# # Streamlit app
# st.title("AI-Generated Image Detector")
# st.write("Upload an image to determine if it is AI-generated or not.")

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     img = Image.open(uploaded_file)
#     st.image(img, caption="Uploaded Image", use_column_width=True)
#     st.write("")
#     st.write("Classifying...")
    
#     prediction = predict(img)
#     if prediction > 0.5:
#         st.write("The image is **AI-generated**.")
#     else:
#         st.write("The image is **not AI-generated**.")

# if st.button('Reload Model'):
#     model = load_model(MODEL_PATH)
#     st.write('Model reloaded!')
