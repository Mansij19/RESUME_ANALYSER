"""
Resume Quality Classifier - Training Script
=============================================
Trains a TF-IDF + Logistic Regression model to classify
resume quality as Good / Average / Poor.

Usage:
    python model/train_model.py

Output:
    model/classifier.pkl       - Trained Logistic Regression model
    model/tfidf_vectorizer.pkl - Fitted TF-IDF vectorizer
"""

import os
import csv
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(SCRIPT_DIR, 'dummy_dataset.csv')
CLASSIFIER_PATH = os.path.join(SCRIPT_DIR, 'classifier.pkl')
VECTORIZER_PATH = os.path.join(SCRIPT_DIR, 'tfidf_vectorizer.pkl')


def load_dataset():
    """Load the labeled resume dataset from CSV."""
    texts = []
    labels = []
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row['resume_text'].strip())
            labels.append(row['quality_label'].strip())
    return texts, labels


def train():
    """Train the model, evaluate, and save to disk."""
    print("=" * 50)
    print("  Resume Quality Classifier - Training")
    print("=" * 50)

    # 1. Load data
    texts, labels = load_dataset()
    print(f"\n[INFO] Loaded {len(texts)} resume samples")
    print(f"[INFO] Label distribution:")
    for label in set(labels):
        count = labels.count(label)
        print(f"       {label}: {count}")

    # 2. TF-IDF Vectorization
    print("\n[INFO] Fitting TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=3000,
        stop_words='english',
        ngram_range=(1, 2),   # Unigrams + bigrams
        min_df=1,
        max_df=0.95
    )
    X = vectorizer.fit_transform(texts)
    print(f"[INFO] Feature matrix shape: {X.shape}")

    # 3. Train Logistic Regression
    print("\n[INFO] Training Logistic Regression classifier...")
    classifier = LogisticRegression(
        max_iter=1000,
        C=1.0,
        class_weight='balanced',  # Handle imbalanced classes
        random_state=42
    )
    classifier.fit(X, labels)

    # 4. Evaluate with cross-validation
    print("\n[INFO] Cross-validation scores:")
    cv_scores = cross_val_score(classifier, X, labels, cv=3, scoring='accuracy')
    print(f"       Accuracy: {cv_scores.mean():.2f} (+/- {cv_scores.std():.2f})")

    # 5. Full classification report
    y_pred = classifier.predict(X)
    print(f"\n[INFO] Classification Report (on training data):")
    print(classification_report(labels, y_pred))

    # 6. Save model and vectorizer
    with open(CLASSIFIER_PATH, 'wb') as f:
        pickle.dump(classifier, f)
    print(f"[INFO] Saved classifier to: {CLASSIFIER_PATH}")

    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"[INFO] Saved vectorizer to: {VECTORIZER_PATH}")

    print("\n" + "=" * 50)
    print("  Training complete!")
    print("=" * 50)


if __name__ == '__main__':
    train()
