"""
Text Preprocessor Service
==========================
Cleans, tokenizes, and lemmatizes resume text for NLP processing.
"""

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data (runs once, silent after first download)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


def clean_text(text):
    """
    Remove noise from resume text: URLs, emails, phone numbers,
    special characters, and extra whitespace.

    Args:
        text (str): Raw resume text.

    Returns:
        str: Cleaned text.
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+\.\S+', '', text)
    # Remove special characters (keep letters, numbers, spaces, and common tech symbols)
    text = re.sub(r'[^a-zA-Z0-9\s\+\#\.\-\/]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text):
    """
    Tokenize, remove stopwords, and lemmatize text.

    Args:
        text (str): Cleaned text.

    Returns:
        list: List of processed tokens.
    """
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    processed = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token.isalpha() and token not in stop_words and len(token) > 1
    ]
    return processed


def preprocess(text):
    """
    Full preprocessing pipeline: clean → tokenize → lemmatize.

    Args:
        text (str): Raw resume text.

    Returns:
        tuple: (cleaned_text: str, tokens: list)
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    return cleaned, tokens
