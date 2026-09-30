# ML RESOLUTION TIME PREDICTOR

import os
import joblib
import pandas as pd
from pathlib import Path

# 1. MODEL PATH

AI_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = AI_DIR / "models" / "resolution_model.pkl"

# 2. LOAD TRAINED MODEL

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        "Resolution model not found: "
        + MODEL_PATH
    )

model = joblib.load(
    MODEL_PATH
)

# 3. PREDICT RESOLUTION TIME

def predict_resolution_time(
    category,
    severity,
    priority
    ):

    # Create input DataFrame

    input_data = pd.DataFrame({

        "category": [category],

        "severity": [severity],

        "priority": [priority]
    })

# ML Prediction

    prediction = model.predict(
        input_data
    )[0]

# Round prediction

    estimated_hours = round(
        float(prediction),
        2
    )

# Prevent negative prediction

    if estimated_hours < 1:

        estimated_hours = 1

# Convert hours to days

    estimated_days = round(
        estimated_hours / 24,
        2
    )

# Human readable format

    if estimated_hours < 24:

        estimated_time = (
            f"{estimated_hours} hours"
        )

    elif estimated_hours == 24:

        estimated_time = "1 day"

    else:

        estimated_time = (
            f"{estimated_days} days"
        )

# RESULT

    return {

        "estimated_hours":
            estimated_hours,

        "estimated_days":
            estimated_days,

        "estimated_time":
            estimated_time,

        "category":
            category,

        "severity":
            severity,

        "priority":
            priority
    }

# 4. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("     ML RESOLUTION PREDICTOR")
    print("===================================")

    category = input(
        "\nEnter category: "
    ).strip()

    severity = input(
        "Enter severity: "
    ).strip()

    priority = input(
        "Enter priority: "
    ).strip()

    result = predict_resolution_time(

        category,

        severity,

        priority
    )

    print("\n===================================")
    print("       ML PREDICTION RESULT")
    print("===================================")

    print(
        "\nCategory:",
        result["category"]
    )

    print(
        "Severity:",
        result["severity"]
    )

    print(
        "Priority:",
        result["priority"]
    )

    print(
        "Predicted Resolution Hours:",
        result["estimated_hours"]
    )

    print(
        "Predicted Resolution Days:",
        result["estimated_days"]
    )

    print(
        "Estimated Resolution Time:",
        result["estimated_time"]
    )

    print("\n===================================")
