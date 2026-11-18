# -*- coding: utf-8 -*-
"""
Machine Learning Training Pipeline for Modalapada 2.0 (Nudi Setu).
Trains a supervised character n-gram dialect classification model
on the curated 3-region dataset (Hubballi-Dharwad, Mangaluru, Uttara Kannada).

Outputs:
- models/dialect_classifier.joblib: Serialized Scikit-Learn Pipeline
- models/eval_metrics.json: Cross-validation accuracy, F1-score, and Confusion Matrix
"""

import os
import json
import csv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

def load_data(filepath="data/dataset.csv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} samples from {filepath}")
    print("Class distribution:")
    print(df['dialect'].value_counts())
    return df['dialect_text'].astype(str).tolist(), df['dialect'].astype(str).tolist()

def train_and_evaluate():
    os.makedirs("models", exist_ok=True)
    
    X, y = load_data("data/dataset.csv")
    
    print("\n--- Training Pipeline Architecture ---")
    print("1. Feature Extractor: Character TF-IDF (n-grams: 2 to 5)")
    print("2. Classifier: Multi-class Logistic Regression with L2 Regularization")
    
    # Character n-grams capture Kannada dialect morphemes (-ಆಕತ್ತಾನ, -ಪೆ, -ವುತ್ತೆ, etc.)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            analyzer='char',
            ngram_range=(2, 5),
            min_df=2,
            sublinear_tf=True
        )),
        ('clf', LogisticRegression(
            C=3.0,
            max_iter=1000,
            random_state=42,
            class_weight='balanced'
        ))
    ])
    
    # 5-Fold Stratified Cross Validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X, y, cv=cv, scoring='accuracy')
    mean_acc = float(np.mean(cv_scores))
    std_acc = float(np.std(cv_scores))
    
    print(f"\n5-Fold Cross Validation Accuracy: {mean_acc*100:.2f}% (+/- {std_acc*100:.2f}%)")
    
    # Cross-validated predictions for confusion matrix
    y_pred = cross_val_predict(pipeline, X, y, cv=cv)
    labels = sorted(list(set(y)))
    cm = confusion_matrix(y, y_pred, labels=labels)
    report_dict = classification_report(y, y_pred, labels=labels, output_dict=True)
    report_text = classification_report(y, y_pred, labels=labels)
    
    print("\n--- Classification Report ---")
    print(report_text)
    
    print("--- Confusion Matrix ---")
    print("Classes:", labels)
    print(cm)
    
    # Fit full model
    pipeline.fit(X, y)
    
    # Extract top distinctive n-gram features per class
    vectorizer = pipeline.named_steps['tfidf']
    clf = pipeline.named_steps['clf']
    feature_names = np.array(vectorizer.get_feature_names_out())
    
    top_features = {}
    for i, label in enumerate(clf.classes_):
        top_indices = np.argsort(clf.coef_[i])[-10:][::-1]
        top_features[label] = [feature_names[idx] for idx in top_indices]
    
    print("\n--- Top Distinctive Dialect Morphemes (N-Grams) ---")
    for label, feats in top_features.items():
        print(f"• {label}: {', '.join(feats[:6])}")
    
    # Save model and metrics
    model_path = os.path.join("models", "dialect_classifier.joblib")
    joblib.dump(pipeline, model_path)
    print(f"\nTrained model successfully saved to: {model_path}")
    
    metrics = {
        "accuracy": round(mean_acc, 4),
        "std_dev": round(std_acc, 4),
        "total_samples": len(X),
        "classes": labels,
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict,
        "top_features": top_features
    }
    
    metrics_path = os.path.join("models", "eval_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(f"Evaluation metrics saved to: {metrics_path}")

if __name__ == "__main__":
    train_and_evaluate()

