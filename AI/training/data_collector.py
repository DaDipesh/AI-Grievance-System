# VERIFIED COMPLAINT DATA COLLECTOR

import csv
import os
from pathlib import Path

AI_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = AI_DIR / "dataset" / "verified_complaints.csv"

# 1. SAVE NEW AI COMPLAINT

def save_verified_complaint(
    complaint_id,
    complaint_text,
    language,
    category_predicted,
    category_verified,
    severity,
    priority,
    department,
    city,
    district,
    area,
    resolution_hours=None
    ):
    """
    Save complaint data into verified_complaints.csv.
    """

    file_exists = os.path.exists(DATASET_PATH)

    with open(
        DATASET_PATH,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Create header if file doesn't exist
        if not file_exists:

            writer.writerow([
                "complaint_id",
                "complaint_text",
                "language",
                "category_predicted",
                "category_verified",
                "severity",
                "priority",
                "department",
                "city",
                "district",
                "area",
                "resolution_hours"
            ])

        writer.writerow([
            complaint_id,
            complaint_text,
            language,
            category_predicted,
            category_verified,
            severity,
            priority,
            department,
            city,
            district,
            area,
            resolution_hours
        ])

# 2. VERIFY COMPLAINT CATEGORY

def verify_category(
    complaint_id,
    verified_category
    ):
    """
    Officer verifies/corrects the AI predicted category.
    """

    if not os.path.exists(DATASET_PATH):

        return {
            "success": False,
            "message": "Dataset file not found."
        }

    rows = []

    found = False

    with open(
        DATASET_PATH,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        fieldnames = reader.fieldnames

        for row in reader:

            if row["complaint_id"] == complaint_id:

                row["category_verified"] = verified_category

                found = True

            rows.append(row)

    if not found:

        return {
            "success": False,
            "message": "Complaint ID not found."
        }

# Rewrite CSV with updated data

    with open(
        DATASET_PATH,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rows)

    return {
        "success": True,
        "message": "Category verified successfully.",
        "complaint_id": complaint_id,
        "category_verified": verified_category
    }

# 3. UPDATE ACTUAL RESOLUTION TIME

def update_resolution_time(
    complaint_id,
    resolution_hours
    ):
    """
    Save actual resolution time after
    the complaint has been resolved.
    """

    if not os.path.exists(DATASET_PATH):

        return {
            "success": False,
            "message": "Dataset file not found."
        }

    rows = []

    found = False

    with open(
        DATASET_PATH,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        fieldnames = reader.fieldnames

        for row in reader:

            if row["complaint_id"] == complaint_id:

                row["resolution_hours"] = resolution_hours

                found = True

            rows.append(row)

    if not found:

        return {
            "success": False,
            "message": "Complaint ID not found."
        }

# Rewrite CSV

    with open(
        DATASET_PATH,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rows)

    return {
        "success": True,
        "message": "Resolution time updated successfully.",
        "complaint_id": complaint_id,
        "resolution_hours": resolution_hours
    }

# 4. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("     COMPLAINT VERIFICATION")
    print("===================================")

    complaint_id = input(
        "\nEnter Complaint ID: "
    ).strip()

    verified_category = input(
        "Enter verified category: "
    ).strip()

    result = verify_category(
        complaint_id,
        verified_category
    )

    print("\nResult:")
    print(result)

# Update actual resolution time

    update_time = input(
        "\nEnter actual resolution hours "
        "(leave blank to skip): "
    ).strip()

    if update_time:

        try:

            resolution_hours = float(
                update_time
            )

            result = update_resolution_time(
                complaint_id,
                resolution_hours
            )

            print("\nResolution Update:")
            print(result)

        except ValueError:

            print(
                "\nInvalid resolution hours."
            )
