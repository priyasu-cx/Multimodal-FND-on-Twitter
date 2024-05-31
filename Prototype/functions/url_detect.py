import re


def detect_url(text):
    pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    urls = re.findall(pattern, text)
    return urls


# Test the function
text = "Check out this cool website: https://www.streamlit.io/"
print(detect_url(text))



