"""
Text Preprocessor Service
==========================
Cleans, tokenizes, and lemmatizes resume text for NLP processing.
"""

import re
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# --- NLTK Setup for Vercel ---
if os.environ.get('VERCEL'):
    nltk_data_dir = '/tmp/nltk_data'
    os.makedirs(nltk_data_dir, exist_ok=True)
    nltk.data.path.append(nltk_data_dir)
else:
    nltk_data_dir = None

# Download required NLTK data
def setup_nltk():
    """Download required NLTK data to the specified directory."""
    for package in ['punkt', 'punkt_tab', 'stopwords', 'wordnet']:
        nltk.download(package, download_dir=nltk_data_dir, quiet=True)

setup_nltk()



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
