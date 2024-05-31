import pickle
import pandas as pd
import re
import os
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the model
# Define the paths to the model and vectorizer files relative to the current script
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'xgboost_model.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'tfidf_vectorizer.pkl')

# Load the XGBoost model
with open(model_path, 'rb') as model_file:
    xgb_model = pickle.load(model_file)

# Load the TF-IDF vectorizer
with open(vectorizer_path, 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)


def predict_fnd(tweet_text, exclusivity, bot_score, cred_score, label_score):
    

    # Vectorization using TF-IDF
    text_tfidf = tfidf_vectorizer.transform([tweet_text])

    # Combine text features with other numerical features
    other_features = sp.csr_matrix([[exclusivity, bot_score, cred_score, label_score]])
    combined_features = sp.hstack((text_tfidf, other_features), format='csr')


    # Perform prediction
    prediction = xgb_model.predict(combined_features)

    return prediction


# Preprocessing functions
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove mentions and hashtags
    text = re.sub(r'@[^\s]+|#[^\s]+', '', text)
    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    return text

# tweet = "This is a fake news tweet"
# exclusivity = 0.8
# bot_score = 0.1
# cred_score = 0.8
# label_score = 5
# prediction = predict_fnd(tweet, exclusivity, bot_score, cred_score, label_score)

# print("Predicted class:", prediction)