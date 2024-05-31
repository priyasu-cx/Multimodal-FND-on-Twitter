import streamlit as st
from functions.fnd_model import predict_fnd
from functions.url_model import predict_url

def main():
    # Set title and color theme
    st.set_page_config(page_title='Fake News Detection on Twitter', layout='wide', initial_sidebar_state='auto')

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
        url_report = predict_url(url)
    

        # Display the report
        if fnd_report == 1:
            st.write("This tweet is fake news.")
        else:
            st.write("This tweet is not fake news.")

        if url_report == 1:
            st.write("This URL is malicious.")
        else:
            st.write("This URL is safe.")

        st.write("Report generated!")

if __name__ == "__main__":
    main()
