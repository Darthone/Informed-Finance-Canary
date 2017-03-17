import re

def preprocess_text(text):
    """ changes text to lowercase and strips special characters/punctuation """
    text = re.sub(r'[^A-Za-z0-9\.]+', ' ', text).strip()
    text = re.sub(r'\.\s', ' ', text)
    return text.lower()

class Document(object):
    """ used to represent articles """

    def __init__(self, text):
        self.text = preprocess_text(text)

    #TODO add other things

