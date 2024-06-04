import streamlit as st
from functions.fnd_model import predict_fnd
from functions.image_model import predict_image
from functions.classify_fnd import getSemantics
from pysafebrowsing import SafeBrowsing
from dotenv import load_dotenv
import os
from PIL import Image
import re


def reset():
    st.session_state.image_uploaded = False
    st.session_state.uploaded_image = None
    st.session_state.fnd_report = None
    st.session_state.url_report = None
    st.session_state.semantics_report = None
    st.session_state.image_report = None
    st.session_state.image = None
    st.session_state.tweet = None

def checkURL(url):
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("PHISHTANK_API_KEY")
    s = SafeBrowsing(api_key)
    r = s.lookup_urls([url])
    if r[url]["malicious"]:
        print("This URL is malicious.")
        return 1
    else:
        print("This URL is not malicious.")
        return 0
    
def fetchURL(tweet):
    # fetch URL from tweet
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, tweet)
    if urls:
        return urls[0]
    return -1

def submit_report(tweet, exclusivity, bot_score, cred_score, label_score, uploaded_image):
    # Perform fake news detection and generate report
    if tweet or uploaded_image is not None:
        fnd_report = int(predict_fnd(tweet, exclusivity, bot_score, cred_score, label_score))
        url = fetchURL(tweet)
        st.session_state.url = url

        # print("URL:", url)
        url_report = 0
        semantics_report = 0
        prediction = 0

        if url != -1:
            # Check URL from Safe Browsing API
            if checkURL(url) == 1:
                # st.write("This URL is malicious.")
                url_report = 1
            else:
                # st.write("This URL is not malicious.")
        
        # Semantics Classifier Report
        if fnd_report == 1: semantics_report = getSemantics(tweet, bot_score, url_report)

        # Display the report
        # if fnd_report == 1:
        #     st.write("This tweet is fake news.")
        # else:
        #     st.write("This tweet is not fake news.")

        # Display the image report
        if uploaded_image is not None:
            img = Image.open(uploaded_image)
            # st.image(img, caption="Uploaded Image", use_column_width=True)
            st.write("")
            st.write("Classifying...")
            
            prediction = predict_image(img)

            
            # if prediction == 1:
            #     st.write("The image is **not AI-generated**.")
            # else:
            #     st.write("The image is **AI-generated**.")

        # st.page_link("pages/report.py", label="Tweet Report", icon="📄")
        print("FND Prediction:", fnd_report)
        print("Image Prediction:", prediction)
        print("URL Prediction:", url_report)
        print("Semantics Prediction:", semantics_report)


        # Load data into session state
        st.session_state.fnd_report = fnd_report
        st.session_state.url_report = url_report
        st.session_state.semantics_report = semantics_report
        st.session_state.image_report = prediction

        if uploaded_image: st.session_state.image = uploaded_image
        if tweet: st.session_state.tweet = tweet

        st.switch_page("pages/report.py")
    else:
        # Display error message
        st.error("Please enter a tweet body.", )

    

    return 0
    
    

def main():
    reset()
    # Set title and color theme
    st.set_page_config(
        page_title="Fake News Detection on Twitter",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # Set title
    st.title("Multimodal Fake News Detection on Twitter")

    st.divider()

    # Set sidebar
    st.sidebar.title("Select a Classifier: ")
    no_sidebar_style = """
        <style>
            div[data-testid="stSidebarNav"] {display: none;}
        </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

    with st.sidebar:
        st.divider()
        # if st.write("<p class=sidebar>Tweet Body Classifier</p>", unsafe_allow_html=True):
        #     st.switch_page("pages/tweetBodyClassifier.py")
        if st.button("Tweet Body Classifier"):
            st.switch_page("pages/tweetBodyClassifier.py")
        st.write(":heavy_minus_sign:" * 10) # horizontal separator line.
        if st.button("URL Classifier"):
            st.switch_page("pages/urlClassifier.py")
        st.write(":heavy_minus_sign:" * 10) # horizontal separator line.
        if st.button("Image Classifier"):
            st.switch_page("pages/imageClassifier.py")
        st.write(":heavy_minus_sign:" * 10) # horizontal separator line.
        if st.button("Semantics Classifier"):
            st.switch_page("pages/semanticsClassifier.py")
        st.markdown("""<style>.sidebar {font-size: 18px;}</style>""", unsafe_allow_html=True)

    # Columns for other features
    main_col1, main_col2 = st.columns(2, gap="medium")

    with main_col2:

        # Make a container
        with st.container(border=True):
            P2_col1, P2_col2 = st.columns([1,8])

            with P2_col1:
                #Insert image in a circle
                st.image("https://i.vgy.me/ghcFZ5.png")

            with P2_col2:
                st.markdown("""
                            <style>
                            .User {
                                font-size: 20px;
                                font-weight: bold;
                            }
                            .username {
                                font-size: 16px;
                                color: grey;
                            }
                            .flex {
                                display: flex;
                                align-items: baseline;
                            }
                            </style>
                            <div class=flex><p class=User>TweetBot&nbsp&nbsp</p><p class=username>&nbsp@iambot &#x2022; Jun 5</p></div>
                            """, unsafe_allow_html=True)

                # Add multiline text input
                tweet = st.text_area("Tweet Body", label_visibility="collapsed", placeholder="Type here")

                if 'image_uploaded' not in st.session_state:
                    st.session_state.image_uploaded = False
                if 'uploaded_image' not in st.session_state:
                    st.session_state.uploaded_image = None

                # Check if an image has been uploaded
                if not st.session_state.image_uploaded:
                    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
                    # uploaded_image = Image.open(uploaded_image) if uploaded_image is not None else None
                    if uploaded_image is not None:
                        st.session_state.image_uploaded = True
                        st.session_state.uploaded_image = uploaded_image

                # Display the uploaded image if one is uploaded
                if st.session_state.image_uploaded:
                    st.image(st.session_state.uploaded_image, use_column_width=True)

                st.write("")

    with main_col1:
        # Title for other features
        st.subheader("Other Input Features")

        # Columns for other features
        col1, col2 = st.columns(2)

        # Add text input
        with col1:

            exclusivity = st.number_input("Exclusivity", step=1, max_value=1, min_value=0)
            bot_score = st.number_input("Bot Score", step=1e-5, format="%.5f")

        with col2:
            cred_score = st.number_input("Credibility Score", step=1e-5, format="%.6f")
            label_score = st.number_input("5 Label Score", step=1, max_value=4, min_value=0)

        # st.subheader("Image Upload")
        # Add image upload
        # uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        # st.subheader("Check URL")
        # # Add text input for URL
        # url = st.text_input("URL", "Type here")

        # st.subheader("Semantics Classifier")
        # # Add text input for URL
        # semantics = st.text_input("Classify Tweet", "Type here")

        # Add Gap
        st.write("<br><br>", unsafe_allow_html=True)

        
        # Add button to generate report
        tc1, tc2, tc3 = st.columns([2, 1, 3.5])
        if tc1.button("Generate Report", type="primary"):
            submit_report(tweet, exclusivity, bot_score, cred_score, label_score, st.session_state.uploaded_image)

        if tc2.button("Reset"):
            reset()
        


    




    

        # Disinformation, Misinformation, Sattire, Spam
        # if fnd_report == 1:
            # if bot_score >= 0.5:
            #     st.write("This tweet is classified as **Disinformation**.")
            # else:
            #     result = classify_FND(fnd_report, tweet)
            #     if result == 1:
            #         st.write("This tweet is classified as **Satire**.")
            #     elif result == 0:
            #         st.write("This tweet is classified as **Spam**.")
            #     else:
            #         st.write("This tweet is classified as **Misinformation**.")
            # getSemantics(semantics, bot_score, checkURL(url))

            # st.write("Semantics Classifier Report generated!")
            # st.write("The tweet is classified as **Yet to be decided**.")


if __name__ == "__main__":
    main()
