# DUPLICATE COMPLAINT DETECTOR

import os
import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

AI_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = AI_DIR / "dataset" / "verified_complaints.csv"

def detect_duplicate(
    complaint_text,
    similarity_threshold=0.70
    ):
    """
    Compare a new complaint with previous
    complaints and detect possible duplicates.
    """

    if not os.path.exists(DATASET_PATH):

        return {
            "is_duplicate": False,
            "similarity": 0,
            "existing_complaint_id": None,
            "message": "No previous complaints found."
        }

    df = pd.read_csv(
        DATASET_PATH
    )

    if df.empty:

        return {
            "is_duplicate": False,
            "similarity": 0,
            "existing_complaint_id": None,
            "message": "No previous complaints found."
        }

    if "complaint_text" not in df.columns:

        return {
            "is_duplicate": False,
            "similarity": 0,
            "existing_complaint_id": None,
            "message": "Complaint text column not found."
        }

    previous_complaints = (
        df["complaint_text"]
        .fillna("")
        .astype(str)
        .tolist()
    )

# Add new complaint to create same TF-IDF space
    all_complaints = (
        previous_complaints
        + [complaint_text]
    )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        all_complaints
    )

    new_vector = vectors[-1]

    previous_vectors = vectors[:-1]

    similarities = cosine_similarity(
        new_vector,
        previous_vectors
    )[0]

    if len(similarities) == 0:

        return {
            "is_duplicate": False,
            "similarity": 0,
            "existing_complaint_id": None,
            "message": "No previous complaints found."
        }

    best_index = similarities.argmax()

    best_similarity = (
        similarities[best_index]
    )

    similarity_percentage = round(
        float(best_similarity * 100),
        2
    )

    existing_id = None

    if "complaint_id" in df.columns:

        existing_id = df.iloc[
            best_index
        ]["complaint_id"]

    if best_similarity >= similarity_threshold:

        return {
            "is_duplicate": True,
            "similarity":
                similarity_percentage,
            "existing_complaint_id":
                existing_id,
            "message":
                "Possible duplicate complaint detected."
        }

    return {
        "is_duplicate": False,
        "similarity":
            similarity_percentage,
        "existing_complaint_id":
            None,
        "message":
            "No duplicate complaint detected."
    }

# TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("     DUPLICATE COMPLAINT DETECTOR")
    print("===================================")

    complaint = input(
        "\nEnter new complaint: "
    ).strip()

    result = detect_duplicate(
        complaint
    )

    print("\n===================================")
    print("             RESULT")
    print("===================================")

    print(
        "\nDuplicate:",
        result["is_duplicate"]
    )

    print(
        "Similarity:",
        result["similarity"],
        "%"
    )

    print(
        "Existing Complaint ID:",
        result["existing_complaint_id"]
    )

    print(
        "Message:",
        result["message"]
    )

    print("\n===================================")
