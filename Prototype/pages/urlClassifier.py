import streamlit as st
from app import predict_url

def tweetBodyClassifier():
    st.set_page_config(page_title="URL Classifier", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")

    st.title("URL Classifier")
    st.divider()

    col11, col21 = st.columns([2, 1], gap="medium")

    result = None


    with col11:
        url = st.text_input("Enter URL")
        st.write("")
        
        if st.button("Generate Report", type="primary"):
            if url:
                result = predict_url(url)
                st.write("Report generated successfully!")
            else:
                st.error("Please enter a URL.", )

    with col21:
        with st.container(border=True, height=300):
            st.write("<center>Results will be displayed here.</center>", unsafe_allow_html=True)
            st.divider()

            if result:
                st.write("<center><p class=result-fake>The url is classified as: <b>Malicious</b></p><center>", unsafe_allow_html=True)
            elif result == 0:
                st.write("<center><p class=result-real>The url is classified as: <br><b>Not Malicious</b></p><center>", unsafe_allow_html=True)

            
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