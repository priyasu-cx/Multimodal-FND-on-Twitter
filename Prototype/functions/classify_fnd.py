from .checkSpam import *
from .checkSattire import *

"""
This function calculates the final result that'll come out of the semantics classifier,
as one of: ["misinformation", "disinformation", "spam", "satire"]
"""


def getSemantics(tweet_body, bot_score, phishingPresent):
    print("Tweet:")
    print(tweet_body + "\n")

    # Possible results from this classifier
    results = ["misinformation", "disinformation", "spam", "satire"]
    final_result = -1

    # Check if the user is a bot
    if bot_score >= 0.5:
        isBot = True
    else:
        isBot = False

    # Final Result will be disinformation if user is a bot
    if isBot:
        print("User is a bot, who has shared false news")
        final_result = results[1]
        print(final_result)
        return

    print(
        "User is not a bot. Not disinformation.\nChecking for type of misinformation...\n"
    )

    # Processing for spam
    isSpam = checkSpam(tweet_body, phishingPresent)

    # Processing for satire
    isSatire = checkSatire(tweet_body)

    # If either one of them is true(1)     => that will the type of misinfo
    # If both of them are true(1)/false(0) => we just say that it's a misinformation
    if (isSpam == 1 and isSatire == 1) or (isSpam == 0 and isSatire == 0):
        print("Couldn't cleary detect whether spam or satire")
        final_result = results[0]

    elif isSpam == 1:
        print("Tweet could be a potential spam!!".upper())
        final_result = results[2]
    else:
        print("Tweet could be a potential satire!!".upper())
        final_result = results[3]

    print("Final outcome: " + final_result)

    return final_result
# Testing the function
# tweet_body= "Hurry!!! Limited period offer: checkout this link @@$www.urlcoms.xyxz"  # spam
# tweet_body= "I was happy that I was late to class. Anyways i'm offering a discount on my time management courses. Check it out here: bitly.com"  # spam
# tweet_body= "I was happy that I was late to class"  # satire
# tweet_body= "Messi just lost the world cup. He's planning on retiring!!"  # misinformation
# getSemantics(tweet_body, bot_score, phishingPresent)
