import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# 1. LOAD DATASET

AI_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = AI_DIR / "models"
data = pd.read_csv(AI_DIR / "dataset" / "complaints.csv")

print("Total complaints:", len(data))

print("\nCategories:")
print(data["category"].value_counts())

# 2. INPUT AND OUTPUT

X = data["complaint"]
y = data["category"]

# 3. TRAIN / TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining complaints:", len(X_train))
print("Testing complaints:", len(X_test))

# 4. WORD TF-IDF

word_vectorizer = TfidfVectorizer(
    analyzer="word",
    ngram_range=(1, 2),
    sublinear_tf=True
)

# 5. CHARACTER TF-IDF

char_vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 5),
    sublinear_tf=True
)

# 6. COMBINE WORD + CHARACTER FEATURES

vectorizer = FeatureUnion([
    ("word", word_vectorizer),
    ("char", char_vectorizer)
])

# 7. TRANSFORM DATA

X_train_vectorized = vectorizer.fit_transform(X_train)

X_test_vectorized = vectorizer.transform(X_test)

# 8. TRAIN MODEL

model = LogisticRegression(
    max_iter=2000,
    C=2.0
)

model.fit(
    X_train_vectorized,
    y_train
)

# 9. PREDICTION

y_pred = model.predict(X_test_vectorized)

# 10. ACCURACY

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n===================================")
print("MODEL PERFORMANCE")
print("===================================")

print(
    "\nAccuracy:",
    round(accuracy * 100, 2),
    "%"
)

# 11. CLASSIFICATION REPORT

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

# 12. SAVE MODEL

joblib.dump(
    model,
    MODELS_DIR / "trained_model.pkl"
)

joblib.dump(
    vectorizer,
    MODELS_DIR / "vectorizer.pkl"
)

print("\n===================================")
print("AI MODEL SUCCESSFULLY TRAINED")
print("===================================")

print("\nModel saved:")
print("models/trained_model.pkl")

print("\nVectorizer saved:")
print("models/vectorizer.pkl")
