from collections import Counter
import string
import nltk
from nltk.corpus import stopwords
import re

# Repetitive Words Score (RWS)

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def count_words(sentence):
    # Remove punctuation and convert to lowercase
    sentence = sentence.translate(str.maketrans('', '', string.punctuation)).lower()
    # Split the sentence into words
    words = sentence.split()
    # Filter out stop words and count occurrences of each word
    word_counts = Counter(word for word in words if word not in stop_words)
    return word_counts

def find_threshold_k(sentence, word_freq):
    # Sort words by frequency in descending order
    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # At the drop-off point, k should be equal to the index i of that word
    # in the sorted list of word frequencies (sorted_word_freq).
    # This index indicates the position of the word in the sorted list,
    # which effectively represents the number of unique words with frequencies higher than
    # or equal to the frequency of the word at the drop-off point.

    # Calculate drop-off point
    k = len(sorted_word_freq)  # Initialize k to the number of unique words

    for i, (word, freq) in enumerate(sorted_word_freq):
        if freq < sorted_word_freq[0][1] / 2:  # Drop-off point: frequency less than half of the most frequent word
            k = i
            break

    # in case of no drop-off point, we know that all the unique words are reapting at a freq very close to one another
    # in such cases, we assume the acceptable range of any word to be 4
    if(k!=len(sorted_word_freq)):
      return k

    max_acceptable_freq= 4
    return max_acceptable_freq

# sentence = "verify add discount  verify add discount, ! @@@ verify add discount  verify add discount  verify add discount"
# sentence= "Hi! we ar eplaesed to announce discount on our latest collection. This discount is for limited time only. Discount is walid till stocks last. Avail your discount today!!"
# word_freq = count_words(sentence)
# k = find_threshold_k(sentence, word_freq)
# print("Threshold value (k):", k)


# This function checks if the freq of any word in the sentence is above a threshold limit or not
# it returns a score of 1(repetitive words exist) or 0
def checkRepetitiveWords(sentence):
  print("Checking repetitive words...")

  # getting the freq of each word
  word_freq = count_words(sentence)

  # finding the threshold based on the freq of words we got
  k = find_threshold_k(sentence, word_freq)
  print("Threshold value (k):", k)

  # calculating score
  for word, count in word_freq.items():
        if count > k:
            return 1
  return 0


# Special Charcter Score (SCC)

# This function removes brackets from a sentence
def remove_brackets(sentence):
    # Define a regular expression pattern to match all types of brackets
    bracket_pattern = r'[()\[\]{}]'

    # Remove all brackets from the sentence
    sentence_without_brackets = re.sub(bracket_pattern, '', sentence)

    return sentence_without_brackets

# This function checks whether a sentence consists of continous sequences of different special characters
def has_different_special_chars(sentence):
    # First remove brackets from the sentence, as they can cause problems in detection
    sentence=  remove_brackets(sentence)

    # Find all continuous sequences of special characters separated by space
    special_sequences = re.findall(r'[^a-zA-Z0-9\s]+', sentence)

    # Iterate through each sequence
    for sequence in special_sequences:
        # Remove non-special characters
        sequence = re.sub(r'[^!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>\/?~`]', '', sequence)

        # Count the number of unique special characters in the sequence
        unique_special_chars = set(sequence)

        # If there are more than one unique special characters in the sequence, return True
        if len(unique_special_chars) > 1:
            print("SPAMMY TEXT DETECTED: " + sequence)
            return True

    # If no sequence with different special characters is found, return False
    return False


"""
# This function detects the excessive use of punctuation marks by
# iterating through each character in the sentence and checking for
# sequences of repeated punctuation marks
"""
def detect_excessive_punctuation(sentence):
    # Regular expression pattern for detecting consecutive punctuation marks
    # we're allowing maximum of 3 consecutive special characters
    # Allowed: ("Hi!!!", "Okay...", etc)
    # Not allowed: ("Hey....", "@@@@..", etc)

    punctuation_pattern = r'([^\w\s])\1{3,}'                  # continuous sequence of same char (@@, !!!, ???)

    # Searching for consecutive punctuation marks in the sentence
    excessive_punctuation_matches = re.findall(punctuation_pattern, sentence)

    # If matches are found, return True (indicating spam)
    if excessive_punctuation_matches or has_different_special_chars(sentence):
        return True, excessive_punctuation_matches
    else:
        return False, []

# This function calculates the special_char_score
def checkSpecialCharacters(sentence):
  print("Cheking special characters...")



  is_spam, excessive_punctuation = detect_excessive_punctuation(sentence)
  if is_spam:
      print("Spam detected! Excessive special characters used:", excessive_punctuation)
      return 1
  else:
      print("No excessive use of special characters found. Not spam.")
      return 0

# Trying out the function
# sentence = "Hello!!! How are you???? I #### @@@@ #$@ @hemlo @yeoeo @hehe @hysdf hope you're doing well..."  # spam(####, &&&&)
# sentence= "How are you Doing?? Are you okayy?"  # not spam
# sentence= "### ---  *^& @@@" # spam(*^&)
# checkSpecialCharacters(sentence)

# Tweet Length Score (TLS)
# This function calculates the no. of characters in a given text
def count_characters(sentence):
    # Calculate the number of characters in the sentence
    return len(sentence)


""" This function checks whether a given tweet body
    is within the range of an average tweet's length(0)
    or not(1)
"""
def checkTweetLength(tweet_body):
  print("Checking tweet length...")
  lowerLimit= 30
  upperLimit= 140
  charCount= count_characters(tweet_body)
  print("Given tweet has " + str(charCount) + " no. of characters")

  if(charCount<lowerLimit or charCount>upperLimit):
    print("Tweet Not in average length range!".upper())
    return 1

  print("Tweet is within the average length range")
  return 0

# Testing the function
# sentence= "Hello world *()@#$^& "
# checkTweetLength(sentence)


# Special Word Score (SWS)
# This function checks whether any of the stored spam words are present in a given sentence or not
def detect_spam(sentence):
    spam_words = [
        "free", "offer", "discount", "limited", "promotion", "sale",
        "click", "now", "urgent", "buy", "exclusive", "win",
        "prize", "cash", "money", "credit", "card", "viagra",
        "loan", "investment", "earn", "income", "guaranteed",
        "risk-free", "weight loss", "diet", "lose weight", "miracle",
        "enhancement", "enlarge", "sex", "dating", "adult",
        "meet singles", "hot", "singles", "satisfaction", "pharmacy",
        "prescription", "medication", "online", "purchase", "order",
        "income", "work from home", "make money", "earn money",
        "investment", "opportunity", "financial freedom", "millionaire",
        "click here", "subscribe", "unsubscribe", "visit our website",
        "visit now", "limited time offer", "call now", "order now",
        "act now", "buy now", "special offer", "bonus", "prizes",
        "debt", "insurance", "claim", "inheritance", "refund",
        "discounted", "cheap", "lowest price", "best price",
        "lowest rates", "lowest mortgage rates", "meet sexy singles",
        "teen", "teenager", "teenage", "teenagers", "weight",
        "pills", "online degree", "university diploma", "diploma",
        "degrees", "drugs", "pharmaceutical", "casino", "gambling",
        "roulette", "betting", "online gambling", "lottery",
        "slots", "poker", "blackjack", "baccarat", "craps",
        "bingo", "jackpot", "loan", "credit", "debt", "cash",
        "cash prize", "winner", "guarantee", "prize claim",
        "financial advice", "stock alert", "stock pick",
        "stock recommendation", "investment advice",
        "penny stocks", "investment opportunity",
        "earn extra income", "earn money online",
        "work from home", "extra cash", "extra income",
        "home based business", "home business",
        "multi-level marketing", "get-rich-quick",
        "make money fast", "money-making scheme",
        "online business", "passive income",
        "start your own business", "work at home",
        "click below", "check this out", "order now",
        "subscribe now", "click to remove",
        "click to unsubscribe", "direct email",
        "email marketing", "increase sales",
        "increase traffic", "internet marketing",
        "marketing solutions", "mass email",
        "bulk email", "email blast", "opt-in email",
        "targeted email", "web traffic", "website traffic"
    ]
    # Convert the sentence to lowercase for case-insensitive matching
    sentence_lower = sentence.lower()

    # Check if any spam word is present in the sentence
    for word in spam_words:
        if word in sentence_lower:
            return True

    return False

"""
  This function detects whether the given text consists any of a certain
  collection of spam words curated from the internet and returns the
  score of 1(potential spam) or 0(not spam)
"""
def checkSpecialWords(sentence):
  print("Checking for special words...")

  if(detect_spam(sentence)):
    print("POTENTIAL SPAM!")
    return 1

  print("Text is free of any spam words")
  return 0

# Testing the function
# sentence= "Hurry, limited period offer"
# detect_spam(sentence)


# Check Spam Score (CSS)
# This function checks whether a given piece of text is spam or not
def checkSpam(tweet_body, phishingPresent):
  # we're using the following factors:
  # repetitive_words_score (0/1)  =>  indicates whether the text contains repetitive words(1) or not (0)
  # special_char_score (0/1)      =>  indicates whether the text contains certain amount of special characters(1) or not(0)
  # tweet_length_score (0/1)      =>  indicates whether the tweet length is longer/shorter compared to an average tweet length(1) or not(0)
  # special_words_score (0/1)     =>  indicates whether the text contains certain words like ["discount", "free",...] over a certain count(1) or not(0)
  # phishing_links_present (0/1)  =>  indicates whether the tweet body consisted of phishing links(1) or not(0)

  print("Checking for Spam...\n")

  # for majority voting amongst the above factors
  total_spam_score= 0
  isSpam= False

  # calculating repetitive_words_score
  repetitive_words_score= checkRepetitiveWords(tweet_body)
  print("repetitive_words_score: " + str(repetitive_words_score) + "\n")
  if(repetitive_words_score==1):
    # giving double the importance to this factor, since it is very rare
    # that someone types a whole another word multiple times by mistake
    total_spam_score+= 2

  # calculating special_char_score
  special_char_score= checkSpecialCharacters(tweet_body)
  print("special_char_score: " + str(special_char_score) + "\n")
  if(special_char_score==1):
    total_spam_score+= 1

  # calculating tweet_length_score
  tweet_length_score= checkTweetLength(tweet_body)
  print("tweet_length_score: " + str(tweet_length_score) + "\n")
  if(tweet_length_score==1):
    total_spam_score+= 1

  # calculating special_words_score
  special_words_score= checkSpecialWords(tweet_body)
  print("special_words_score: " + str(special_words_score) + "\n")
  if(special_words_score==1):
    # giving double the importance to this factor, since presence of spam words is very indicative
    # towards a piece of text being potential spam
    total_spam_score+= 3

  # calculating phishing_links_present
  phishing_links_present= 0
  if(phishingPresent):
    phishing_links_present= 1
  print("phishing_links_present: " + str(phishing_links_present) + "\n")
  if(phishing_links_present==1):
    # if phishing links are present, it'll anyway be spam
    isSpam= True
    total_spam_score+= 1

  print("total_spam_score: " + str(total_spam_score) + "\n")

  if(total_spam_score>=3 or isSpam):
    print("Majority factors indicate a potential spam")
    return 1

  print("Very few factors indicated the potential for a spam")
  return 0

# Testing out the function
# sentence= "visited visited visited visited visited visited @@@@ ## $$ @@" # Spam
# sentence= "hello twitter. How are you doing today??"  # Not spam
# sentence= "Hurry Limited period offer: Buy 1 get 7 free!"  # spam
# checkSpam(sentence, False)