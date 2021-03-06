import re
import pandas as pd
from nltk import (corpus, tokenize, download)
from unidecode import unidecode
from encoding import encode_labels

download("stopwords")
download('punkt')


def remove_contractions(s):
    # TODO: See if we can find more contractions.
    contractions = [
        ("c/u", "cada uno"),
        ("c/", "con"),
        ("p/", "para"),
    ]
    for expression, replacement in contractions:
        s = s.replace(expression, replacement)
    return s


def remove_numbers(s):
    numbers = r"\d+"
    return re.sub(numbers, "", s)


def remove_symbols(s):
    symbols = r"[^a-zA-Z ]"
    return re.sub(symbols, "", s)


def remove_stopwords(s, language):
    s = ' '.join(w for w in tokenize.word_tokenize(s)
                 if not w in corpus.stopwords.words(language))
    return s


def clean_text(s: str, language: str) -> str:
    """
    Given a string @s and its @language the following parsing is performed:
        - Lowercase letters.
        - Removes non-ascii characters.
        - Removes numbers and special symbols.
        - Expand common contractions.
        - Removes stopwords.
    """
    s = unidecode(s)
    s = s.lower()
    s = remove_contractions(s)
    s = remove_numbers(s)
    s = remove_symbols(s)
    s = remove_stopwords(s, language)
    return s


def preprocess_data(df):
    # Remove numbers, symbols, special chars, contractions, etc.
    cleaned_title_col = df[["title", "language"
                                      ]].apply(lambda x: clean_text(*x),
                                               axis=1)
    # Add @cleaned_title column to df
    df = df.assign(cleaned_title=cleaned_title_col)
    df = df.assign(
        encoded_category=encode_labels(df["category"]))
    df = df.dropna()
    return df