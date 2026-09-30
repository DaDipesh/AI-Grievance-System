# VERIFIED CATEGORY MODEL RETRAINING

import os
import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# PATHS

AI_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = AI_DIR / "models"
VERIFIED_DATASET = AI_DIR / "dataset" / "verified_complaints.csv"

MODEL_PATH = MODELS_DIR / "trained_model.pkl"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.pkl"

# LOAD VERIFIED DATA

if not os.path.exists(VERIFIED_DATASET):

    print("\nERROR:")
    print("verified_complaints.csv not found.")
    print("Expected location:")
    print(VERIFIED_DATASET)
    exit()

df = pd.read_csv(
    VERIFIED_DATASET
)

print("\n===================================")
print("   VERIFIED MODEL RETRAINING")
print("===================================")

print("\nTotal records:", len(df))

# CHECK REQUIRED COLUMNS

required_columns = [
    "complaint_text",
    "category_predicted",
    "category_verified"
]

for column in required_columns:

    if column not in df.columns:

        print(
            f"\nERROR: Missing column: {column}"
        )

        exit()

# USE ONLY VERIFIED RECORDS

df["category_verified"] = (
    df["category_verified"]
    .fillna("")
    .astype(str)
    .str.strip()
)

verified_df = df[
    df["category_verified"] != ""
].copy()

print(
    "Verified records:",
    len(verified_df)
)

# CHECK MINIMUM DATA

if len(verified_df) < 2:

    print("\nNot enough verified data.")
    print(
        "At least 2 verified complaints are "
        "required before retraining."
    )

    print(
        "\nCurrent verified records:",
        len(verified_df)
    )

    print(
        "\nNo existing model was changed."
    )

    exit()

# CHECK NUMBER OF CATEGORIES

number_of_categories = (
    verified_df["category_verified"]
    .nunique()
)

print(
    "Verified categories:",
    number_of_categories
)

if number_of_categories < 2:

    print(
        "\nOnly one category is currently verified."
    )

    print(
        "At least 2 different categories are "
        "required to train a classification model."
    )

    print(
        "\nAdd verified complaints from other "
        "categories and run this script again."
    )

    print(
        "\nNo existing model was changed."
    )

    exit()

# DISPLAY CATEGORY COUNTS

print("\nVerified category distribution:")

print(
    verified_df["category_verified"]
    .value_counts()
)

# PREPARE DATA

X = (
    verified_df["complaint_text"]
    .fillna("")
    .astype(str)
)

y = (
    verified_df["category_verified"]
    .astype(str)
)

# CHECK CLASS COUNTS

class_counts = y.value_counts()

minimum_class_count = class_counts.min()

if minimum_class_count < 2:

    print(
        "\nNot enough samples per category."
    )

    print(
        "Each category needs at least "
        "2 verified complaints for the "
        "evaluation split."
    )

    print(
        "\nCurrent category counts:"
    )

    print(class_counts)

    print(
        "\nNo existing model was changed."
    )

    exit()

# TRAIN / TEST SPLIT

# With very small datasets, use a conservative
# test size while ensuring every class can remain
# represented in the training data.

test_size = max(
    number_of_categories,
    int(round(len(verified_df) * 0.20))
)

if test_size >= len(verified_df):

    test_size = number_of_categories

if (
    len(verified_df) - test_size
    < number_of_categories
):

    print(
        "\nNot enough verified records for "
        "a reliable train/test split."
    )

    print(
        "Add more verified complaints before "
        "retraining."
    )

    print(
        "\nNo existing model was changed."
    )

    exit()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# WORD + CHARACTER TF-IDF

vectorizer = FeatureUnion(
    [
        (
            "word_tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                sublinear_tf=True
            )
        ),

        (
            "char_tfidf",
            TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 5),
                sublinear_tf=True
            )
        )
    ]
)

# TRANSFORM TEXT

X_train_vectorized = vectorizer.fit_transform(
    X_train
)

X_test_vectorized = vectorizer.transform(
    X_test
)

# TRAIN MODEL

model = LogisticRegression(
    max_iter=2000,
    C=2.0
)

print(
    "\nTraining new Logistic Regression model..."
)

model.fit(
    X_train_vectorized,
    y_train
)

# EVALUATE MODEL

predictions = model.predict(
    X_test_vectorized
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    "\nNew Model Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

# SAVE NEW MODEL

os.makedirs(
    MODELS_DIR,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    vectorizer,
    VECTORIZER_PATH
)

print("\n===================================")
print("     RETRAINING COMPLETED")
print("===================================")

print(
    "\nNew model saved:"
)

print(
    MODEL_PATH
)

print(
    "\nNew vectorizer saved:"
)

print(
    VECTORIZER_PATH
)

print(
    "\nTraining was based ONLY on "
    "officer-verified categories."
)
