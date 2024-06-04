from functions.url_feature_extraction import featureExtraction
import pickle
import os
import numpy as np
import streamlit as st


def predict_url(url):
    # Extract features from URL
    print(url)
    features = featureExtraction(url)

    # Ensure features are in the correct format
    if not isinstance(features, (list, np.ndarray)):
        raise ValueError("The extracted features must be a list or numpy array.")
    
    # Convert features to numpy array and reshape if necessary
    features = np.array(features).reshape(1, -1)

    # Load Model
    url_model_path = os.path.join(
        os.path.dirname(__file__), "..", "models", "url_xgboost_model_v2.pkl"
    )

    # url_xgboost_model.pkl
    # Load the URL XGBoost model


    with open(url_model_path, "rb") as url_model_file:
        url_model = pickle.load(url_model_file)

    print(features)

    # Perform prediction
    prediction = url_model.predict(features)

    return [features, prediction]

# Test the function
# url = "https://www.streamlit.io/"
# predict_url(url)
