import streamlit as st
from app import predict_image
from PIL import Image

def tweetBodyClassifier():
    st.set_page_config(page_title="Image Classifier", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")

    st.title("Image Classifier")
    st.divider()

    col11, col21 = st.columns([2, 1], gap="medium")

    result = None


    with col11:
        # Add image upload
        image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        image = Image.open(image) if image else None
        st.write("")
        
        if st.button("Generate Report", type="primary"):
            if image:
                result = predict_image(image)
                print("Result:", result)
                st.write("Report generated successfully!")
            else:
                st.error("Please upload an image.", )

    with col21:
        with st.container(border=True, height=300):
            st.write("<center>Results will be displayed here.</center>", unsafe_allow_html=True)
            st.divider()

            if result == 0:
                st.write("<center><p class=result-fake>The image is classified as: <b>Fake</b></p><center>", unsafe_allow_html=True)
            elif result == 1:
                st.write("<center><p class=result-real>The image is classified as: <br><b>Real</b></p><center>", unsafe_allow_html=True)

            
    if st.button("Back to Home"):
        st.switch_page("app.py")
        


    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        .result-fake {
            color: #ff0000;
            font-size: 1.5em;
        }
        .result-real {
            color: #00ff00;
            font-size: 1.5em;
        }
        
    </style>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    tweetBodyClassifier()