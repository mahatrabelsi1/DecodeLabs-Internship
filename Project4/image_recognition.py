from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class RecognitionResult:
    sample_index: int
    actual_digit: int
    predicted_digit: int
    confidence: float


def load_digit_data():
    digits = load_digits()
    return digits.data, digits.target, digits.images


def build_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", KNeighborsClassifier(n_neighbors=5)),
        ]
    )


def train_model(random_state: int = 42):
    X, y, images = load_digit_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=random_state,
        stratify=y,
    )

    model = build_model()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, X, y, images, X_test, y_test, y_pred, accuracy


def recognize_sample(sample_index: int = 25) -> RecognitionResult:
    model, X, y, *_ = train_model()

    sample_index = sample_index % len(X)
    prediction = int(model.predict([X[sample_index]])[0])
    probabilities = model.predict_proba([X[sample_index]])[0]
    confidence = float(probabilities[prediction])

    return RecognitionResult(
        sample_index=sample_index,
        actual_digit=int(y[sample_index]),
        predicted_digit=prediction,
        confidence=confidence,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DecodeLabs Project 4: basic handwritten digit image recognition."
    )
    parser.add_argument(
        "--sample-index",
        type=int,
        default=25,
        help="Index of the sample digit image to recognize.",
    )
    args = parser.parse_args()

    _, _, _, _, _, y_test, y_pred, accuracy = train_model()
    result = recognize_sample(args.sample_index)

    print("DecodeLabs Project 4 - Image Recognition")
    print("=" * 44)
    print(f"Model accuracy on test data: {accuracy:.2%}")
    print(f"Sample index: {result.sample_index}")
    print(f"Actual digit: {result.actual_digit}")
    print(f"Predicted digit: {result.predicted_digit}")
    print(f"Prediction confidence: {result.confidence:.2%}")
    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()
