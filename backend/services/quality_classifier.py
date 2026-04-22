"""
Resume Quality Classifier Service
===================================
Loads a pre-trained TF-IDF + Logistic Regression model
and classifies resume quality as Good / Average / Poor.
"""

import pickle
import os
from backend.config import CLASSIFIER_PATH, VECTORIZER_PATH

# Module-level cache for the loaded model
_model = None
_vectorizer = None


def load_model():
    """
    Load the trained classifier and TF-IDF vectorizer from disk.
    Models are cached after first load for performance.

    Returns:
        tuple: (classifier, vectorizer)

    Raises:
        FileNotFoundError: If model files don't exist (need to run train_model.py).
    """
    global _model, _vectorizer

    if _model is None or _vectorizer is None:
        if not os.path.exists(CLASSIFIER_PATH):
            raise FileNotFoundError(
                "Model not found! Run 'python model/train_model.py' first."
            )
        with open(CLASSIFIER_PATH, 'rb') as f:
            _model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            _vectorizer = pickle.load(f)

    return _model, _vectorizer


def classify(text):
    """
    Classify resume quality using the pre-trained model.

    Args:
        text (str): Preprocessed resume text.

    Returns:
        dict: {
            'label': str ('Good'/'Average'/'Poor'),
            'confidence': float (0-100),
            'score': int (0-100 quality score)
        }
    """
    model, vectorizer = load_model()

    # Transform text to TF-IDF vector
    X = vectorizer.transform([text])

    # Predict class and probabilities
    label = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    confidence = round(max(proba) * 100, 1)

    # Map label to a base quality score
    score_map = {
        "Good": 85,
        "Average": 60,
        "Poor": 35
    }
    base_score = score_map.get(label, 50)

    # Adjust score slightly based on confidence
    score = min(100, max(0, base_score + int((confidence - 50) * 0.2)))

    return {
        "label": label,
        "confidence": confidence,
        "score": score
    }
