import streamlit as st
from app import predict_fnd

def tweetBodyClassifier():
    st.set_page_config(page_title="Tweet Body Classifier", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")

    st.title("Tweet Body Classifier")
    st.divider()

    col11, col21 = st.columns([2, 1], gap="medium")

    result = None


    with col11:
        tweet = st.text_area("Enter Tweet Body", height=150)
        st.write("")
        # Title for other features
        st.subheader("Other Input Features")

        # Columns for other features
        col1, col2 = st.columns(2)

        # Add text input
        with col1:

            exclusivity = st.number_input("Exclusivity", step=1e-6, format="%.2f")
            bot_score = st.number_input("Bot Score", step=1e-6, format="%.2f")

        with col2:
            cred_score = st.number_input("Credibility Score", step=1e-6, format="%.2f")
            label_score = st.number_input("5 Label Score", step=1e-6, format="%.2f")

        st.write("")
        if st.button("Generate Report", type="primary"):
            if tweet:
                result = predict_fnd(tweet, exclusivity, bot_score, cred_score, label_score)
                st.write("Report generated successfully!")
            else:
                st.error("Please enter a Tweet.", )

    with col21:
        with st.container(border=True, height=300):
            st.write("<center>Results will be displayed here.</center>", unsafe_allow_html=True)
            st.divider()

            if result:
                st.write("<center><p class=result-fake>The tweet is classified as: <b>Fake News</b></p><center>", unsafe_allow_html=True)
            elif result == 0:
                st.write("<center><p class=result-real>The tweet is classified as: <br><b>Real News</b></p><center>", unsafe_allow_html=True)

            
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