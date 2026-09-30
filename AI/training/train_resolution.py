# RESOLUTION TIME ML MODEL TRAINING

import os
import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

# 1. FILE PATHS

AI_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = AI_DIR / "models"
DATASET_PATH = AI_DIR / "dataset" / "resolution_data.csv"

MODEL_PATH = MODELS_DIR / "resolution_model.pkl"

# 2. CHECK DATASET

if not os.path.exists(DATASET_PATH):

    print("\nERROR:")
    print(
        f"Dataset not found: {DATASET_PATH}"
    )

    print(
        "\nFirst create resolution_data.csv"
    )

    exit()

# 3. LOAD DATASET

df = pd.read_csv(
    DATASET_PATH
)

print("\n===================================")
print("   RESOLUTION MODEL TRAINING")
print("===================================")

print(
    "\nDataset Shape:",
    df.shape
)

print(
    "\nColumns:",
    list(df.columns)
)

# 4. REQUIRED COLUMNS

required_columns = [

    "category",

    "severity",

    "priority",

    "resolution_hours"
]

for column in required_columns:

    if column not in df.columns:

        print(
            f"\nERROR: Missing column: {column}"
        )

        exit()

# 5. INPUT AND TARGET

X = df[
    [
        "category",
        "severity",
        "priority"
    ]
]

y = df[
    "resolution_hours"
]

# 6. PREPROCESSING

categorical_features = [

    "category",
    "severity",
    "priority"
]

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features
        )
    ]
)

# 7. RANDOM FOREST MODEL

model = RandomForestRegressor(

    n_estimators=200,

    random_state=42,

    max_depth=10
)

# 8. CREATE PIPELINE

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )
    ]
)

# 9. TRAIN / TEST SPLIT

X_train, X_test, y_train, y_test = (
    train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42
    )
)

print(
    "\nTraining records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)

# 10. TRAIN MODEL

print(
    "\nTraining Random Forest..."
)

pipeline.fit(
    X_train,
    y_train
)

# 11. TEST MODEL

predictions = pipeline.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(
    "\nMean Absolute Error:",
    round(mae, 2),
    "hours"
)

# 12. CREATE MODELS DIRECTORY

os.makedirs(
    MODELS_DIR,
    exist_ok=True
)

# 13. SAVE MODEL

joblib.dump(

    pipeline,

    MODEL_PATH
)

print(
    "\nModel saved successfully:"
)

print(
    MODEL_PATH
)

print("\n===================================")
print("       TRAINING COMPLETED")
print("===================================")
