import streamlit as st
from app import getSemantics

def semanticsClassifier():
    st.set_page_config(page_title="Semantics Classifier", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")

    st.title("Semantics Classifier")
    st.divider()

    col11, col21 = st.columns([2, 1], gap="medium")

    result = None


    with col11:
        tweet = st.text_area("Enter Tweet Body", height=150)

        tc1, tc2 = st.columns(2)
        with tc2:
            url_report = st.number_input("URL Check", step=1, max_value=1, min_value=0)
        with tc1:
            bot_score = st.number_input("Bot Score", step=1e-5, format="%.5f")
        
        st.write("")
        if st.button("Generate Report", type="primary"):
            if tweet:
                result = getSemantics(tweet, bot_score, url_report)
                st.write("Report generated successfully!")
            else:
                st.error("Please enter a Tweet.", )

    with col21:
        with st.container(border=True, height=300):
            st.write("<center>Results will be displayed here.</center>", unsafe_allow_html=True)
            st.divider()

            if result:
                st.write(f"<center><p class=result-real>The tweet is classified as: <b class=result-fake>{result}</b></p><center>", unsafe_allow_html=True)

            
    if st.button("Back to Home"):
        st.switch_page("app.py")
        


    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        .result-fake {
            color: blue;
            font-size: 1.3em;
        }
        .result-real {
            font-size: 1.5em;
        }
        
    </style>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    semanticsClassifier()