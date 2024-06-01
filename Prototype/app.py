import streamlit as st
from functions.fnd_model import predict_fnd
from functions.url_model import predict_url
from functions.image_model import predict_image
from pysafebrowsing import SafeBrowsing
from dotenv import load_dotenv
import os
from PIL import Image


def checkURL(url):
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("PHISHTANK_API_KEY")
    s = SafeBrowsing(api_key)
    r = s.lookup_urls([url])
    if r[url]["malicious"]:
        return 1
    else:
        return 0


def main():
    # Set title and color theme
    st.set_page_config(
        page_title="Fake News Detection on Twitter",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # Set title
    st.title("Multimodal Fake News Detection on Twitter")

    # Add multiline text input
    tweet = st.text_area("Tweet Body", "Type here")

    # Title for other features
    st.subheader("Other Features")

    # Columns for other features
    col1, col2 = st.columns(2)

    # Add text input
    with col1:

        exclusivity = st.number_input("Exclusivity", step=1e-6, format="%.2f")
        bot_score = st.number_input("Bot Score", step=1e-6, format="%.2f")

    with col2:
        cred_score = st.number_input("Credibility Score", step=1e-6, format="%.2f")
        label_score = st.number_input("5 Label Score", step=1e-6, format="%.2f")

    st.subheader("Image Upload")
    # Add image upload
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    st.subheader("Check URL")
    # Add text input for URL
    url = st.text_input("URL", "Type here")

    # Add button to generate report
    if st.button("Generate Report"):
        # Perform fake news detection and generate report
        # Replace this with your own code to generate the report
        fnd_report = predict_fnd(tweet, exclusivity, bot_score, cred_score, label_score)
        # url_report = predict_url(url)

        # Check URL from Safe Browsing API
        if checkURL(url) == 1:
            st.write("This URL is malicious.")
        else:
            st.write("This URL is not malicious.")


        # Display the report
        if fnd_report == 1:
            st.write("This tweet is fake news.")
        else:
            st.write("This tweet is not fake news.")

        st.write("Report generated!")

        # Display the image report
        if uploaded_image is not None:
            img = Image.open(uploaded_image)
            # st.image(img, caption="Uploaded Image", use_column_width=True)
            st.write("")
            st.write("Classifying...")
            
            prediction = predict_image(img)

            print(prediction)

            if prediction == 1:
                st.write("The image is **not AI-generated**.")
            else:
                st.write("The image is **AI-generated**.")
            # if prediction > 0.5:
            #     st.write("The image is **AI-generated**.")
            # else:
            #     st.write("The image is **not AI-generated**.")


if __name__ == "__main__":
    main()
