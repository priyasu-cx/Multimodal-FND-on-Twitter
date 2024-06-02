import nltk
import requests
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to split sentence into subsentences based on sentiment
def split_sentence(sentence):
    subsentences = []
    words = nltk.word_tokenize(sentence)
    current_subsentence = []
    sentiment_score = 0

    # # Iterate through words in the sentence
    # for word in words:
    #     current_subsentence.append(word)
    #     sentiment_score += sia.polarity_scores(word)['compound']

    #     # If sentiment score changes sign, start a new subsentence
    #     if sentiment_score > 0:
    #         subsentences.append(' '.join(current_subsentence))
    #         current_subsentence = []
    #         sentiment_score = 0


    # Iterate through words in the sentence
    for word in words:
        current_subsentence.append(word)
        word_sentiment = sia.polarity_scores(word)['compound']
        # print(word + " score: " + str(sia.polarity_scores(word)['compound']))
        sentiment_score += word_sentiment

        # If sentiment score changes sign or a sentiment word is encountered, start a new subsentence
        if sentiment_score != 0 or word_sentiment != 0:
            subsentences.append(' '.join(current_subsentence))
            current_subsentence = []
            sentiment_score = 0

    # Add the last subsentence if not empty
    if current_subsentence:
        subsentences.append(' '.join(current_subsentence))

    return subsentences


# Testing out the function
# Example sentences
# sentences = [
#     "my flight is delayed and i couldn't be more happier",
# ]

# # Split each sentence into subsentences
# for sentence in sentences:
#     subsentences = split_sentence(sentence)
#     print("Original Sentence:", sentence)
#     print("Subsentences:", subsentences)
#     print()



def getSentiment(text):

  response = requests.get(
      "https://tweetnlp.org/sentiment_data/?model_name=cardiffnlp%2Ftwitter-roberta-base-sentiment-latest&text="
      + text
      + "&is_url=false"
  )

  result = response.json()['data'][0][0]['label']
  # neutral = response.json()['data'][0][1]['score']
  # negative = response.json()['data'][0][2]['score']

  # result = compare_floats(positive, neutral, negative)
  # return result
  return {'label': result}

  # print(response.json()['data'][0])


# This function takes in an array of sentences (Output of the split_sentence() function)
# and then checks if we have both +ve & -ve sentiments
# present in these sentences(1) or not(0)
def findSentiments(sentences):
  positive= False
  negative= False
  for sentence in sentences:
    sentiment= getSentiment(sentence)
    print('"' + sentence + '"')
    print(sentiment["label"]+ "\n")

    if(sentiment["label"]=="positive"):
      positive= True
    elif(sentiment["label"]=="negative"):
      negative= True

  if(positive and negative):
    print("Potential satire (1)\n\n")
    return 1
  else:
    print("Doesn't feel like satire to me :/ (0)\n\n")
    return 0


# Testing out the function
# sentences = ['My mood changes from happy', ', to sad', 'and then happy', 'again']
# sentences= ["I splilled my ice cream and I 'm so happy", 'about it']
# sentences= ['I am happy', 'that I got late to class']
# findSentiments(sentences)


"""
This function takes in the tweet body and breaks in into subsentences
based on the presence of appropriate sentiments
and then checks if the given tweetbody is a potential satire or not
"""
def checkSatire(tweetBody):
  # need to split tweetBody into subsentences
  subsentences = split_sentence(tweetBody)
  print(subsentences)

  satireResult= findSentiments(subsentences)
  return satireResult