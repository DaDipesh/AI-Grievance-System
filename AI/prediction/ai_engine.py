# AI GRIEVANCE ENGINE

# UTF-8 OUTPUT CONFIGURATION

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path

# Resolve project modules and assets from this file, not the caller's cwd.
AI_DIR = Path(__file__).resolve().parents[1]
if str(AI_DIR) not in sys.path:
    sys.path.insert(0, str(AI_DIR))

import uuid
import joblib

from preprocessing.complaint_analyzer import analyze_complaint
from preprocessing.clarification_engine import generate_clarification
from preprocessing.language_detector import detect_language
from preprocessing.severity_predictor import predict_severity
from preprocessing.duplicate_detector import detect_duplicate

from prediction.priority_engine import predict_priority
from prediction.routing_engine import route_complaint
from prediction.response_generator import generate_response
from prediction.resolution_predictor import predict_resolution_time

from training.data_collector import save_verified_complaint

from image.image_analyzer import analyze_image

# 1. LOAD TRAINED ML MODEL

model = joblib.load(AI_DIR / "models" / "trained_model.pkl")

vectorizer = joblib.load(AI_DIR / "models" / "vectorizer.pkl")

# 2. ML CATEGORY PREDICTION

def ml_predict(complaint):

    complaint_vector = vectorizer.transform(
        [complaint]
    )

    prediction = model.predict(
        complaint_vector
    )[0]

    probabilities = model.predict_proba(
        complaint_vector
    )[0]

    confidence = max(probabilities) * 100

    return prediction, confidence

# 3. MAIN AI ANALYSIS

def analyze_with_ai(
    complaint,
    city=None,
    district=None,
    area=None,
    image_path=None,
    save_to_dataset=True
    ):

    # STEP 1: LANGUAGE DETECTION

    language = detect_language(
        complaint
    )

# STEP 2: COMPLAINT ANALYSIS

    analyzer_result = analyze_complaint(
        complaint
    )

# STEP 3: CLARIFICATION

    clarification = generate_clarification(
        complaint
    )

# STEP 4: CHECK PROBLEM

    if not analyzer_result["problem_detected"]:

        return {
            "status": "incomplete",
            "language": language,
            "category": None,
            "category_source": None,
            "ml_prediction": None,
            "ml_confidence": 0,
            "problem_detected": False,
            "duration": analyzer_result["duration"],
            "severity": None,
            "severity_reason": None,
            "priority": None,
            "priority_reason": None,
            "priority_duration_days": 0,
            "department": None,
            "team": None,
            "routing_status": None,
            "city": city,
            "district": district,
            "area": area,
            "resolution_time": None,
            "resolution_hours": None,
            "resolution_days": None,
            "duplicate_result": None,
            "image_result": None,
            "ambiguous": analyzer_result["ambiguous"],
            "needs_clarification":
                clarification["needs_clarification"],
            "clarification_question":
                clarification["question"],
            "reason":
                clarification["reason"],
            "response": None,
            "complaint_id": None,
            "dataset_saved": False
        }

# STEP 5: ML CATEGORY PREDICTION

    ml_category, ml_confidence = ml_predict(
        complaint
    )

# STEP 6: RULE-BASED CATEGORY

    rule_category = (
        analyzer_result["category"]
    )

# STEP 7: FINAL CATEGORY

    if (
        rule_category is not None
        and rule_category != "Ambiguous"
    ):

        final_category = rule_category
        category_source = "Rule-Based"

    else:

        final_category = ml_category
        category_source = "ML"

# STEP 8: SEVERITY

    severity_result = predict_severity(
        complaint,
        final_category
    )

    severity = severity_result[
        "severity"
    ]

    severity_reason = severity_result[
        "reason"
    ]

# STEP 9: PRIORITY

    priority_result = predict_priority(
        complaint,
        severity,
        final_category
    )

    priority = priority_result[
        "priority"
    ]

    priority_reason = priority_result[
        "priority_reason"
    ]

    priority_duration_days = (
        priority_result["duration_days"]
    )

# STEP 10: DEPARTMENT ROUTING

    routing_result = route_complaint(
        final_category,
        city,
        district,
        area
    )

    department = routing_result[
        "department"
    ]

    team = routing_result[
        "team"
    ]

    routing_status = routing_result[
        "routing_status"
    ]

# STEP 11: RESOLUTION TIME

    resolution_result = (
        predict_resolution_time(
            final_category,
            severity,
            priority
        )
    )

    resolution_time = (
        resolution_result["estimated_time"]
    )

    resolution_hours = (
        resolution_result["estimated_hours"]
    )

    resolution_days = (
        resolution_result["estimated_days"]
    )

# STEP 12: DUPLICATE DETECTION

    duplicate_result = detect_duplicate(
        complaint
    )

# STEP 13: IMAGE ANALYSIS

    image_result = None

    if image_path:

        image_result = analyze_image(
            image_path
        )

# STEP 14: MULTILINGUAL RESPONSE

    response = generate_response(
        language,
        final_category,
        severity,
        priority,
        department,
        team,
        analyzer_result["duration"]
    )

# STEP 15: SAVE AI RESULT
    #
    # AI prediction is stored in
    # category_predicted.
    #
    # category_verified remains blank until
    # an officer verifies the complaint.
    #
    # resolution_hours remains blank until
    # the complaint is actually resolved.

    complaint_id = (
        "CMP-" +
        uuid.uuid4().hex[:8].upper()
    )

    if save_to_dataset:

        try:

            save_verified_complaint(
                complaint_id=complaint_id,
                complaint_text=complaint,
                language=language,
                category_predicted=final_category,
                category_verified="",
                severity=severity,
                priority=priority,
                department=department,
                city=city,
                district=district,
                area=area,
                resolution_hours=""
            )

            dataset_saved = True

        except Exception as error:

            dataset_saved = False

            print(
                "\nWARNING: Complaint could not "
                "be saved to verified_complaints.csv"
            )

            print("Reason:", error)

    else:

        dataset_saved = False

# STEP 16: FINAL RESULT

    return {

        "status": "success",

        "language": language,

        "category": final_category,

        "category_source": category_source,

        "ml_prediction": ml_category,

        "ml_confidence": round(
            ml_confidence,
            2
        ),

        "problem_detected":
            analyzer_result["problem_detected"],

        "duration":
            analyzer_result["duration"],

        "severity": severity,

        "severity_reason": severity_reason,

        "priority": priority,

        "priority_reason": priority_reason,

        "priority_duration_days":
            priority_duration_days,

        "department": department,

        "team": team,

        "routing_status": routing_status,

        "city": city,

        "district": district,

        "area": area,

        "resolution_time":
            resolution_time,

        "resolution_hours":
            resolution_hours,

        "resolution_days":
            resolution_days,

        "duplicate_result":
            duplicate_result,

        "image_result":
            image_result,

        "ambiguous":
            analyzer_result["ambiguous"],

        "rule_category":
            rule_category,

        "needs_clarification":
            clarification["needs_clarification"],

        "clarification_question":
            clarification["question"],

        "reason":
            clarification["reason"],

        "response":
            response,

        "complaint_id":
            complaint_id,

        "dataset_saved":
            dataset_saved
    }

# 4. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("       AI GRIEVANCE ENGINE")
    print("===================================")

    complaint = input(
        "\nEnter complaint: "
    ).strip()

    city = input(
        "Enter city (optional): "
    ).strip()

    district = input(
        "Enter district (optional): "
    ).strip()

    area = input(
        "Enter area (optional): "
    ).strip()

    image_path = input(
        "Enter image path (optional): "
    ).strip()

    if image_path == "":
        image_path = None

    result = analyze_with_ai(
        complaint,
        city if city else None,
        district if district else None,
        area if area else None,
        image_path
    )

# DISPLAY RESULT

    print("\n===================================")
    print("          FINAL AI RESULT")
    print("===================================")

    display_fields = [
        ("Status", "status", "\n"),
        ("Complaint ID", "complaint_id", None),
        ("Language", "language", None),
        ("Problem Detected", "problem_detected", None),
        ("Final Category", "category", None),
        ("Category Source", "category_source", None),
        ("ML Prediction", "ml_prediction", None),
        ("ML Confidence", "ml_confidence", "%"),
        ("Duration", "duration", None),
        ("Severity", "severity", None),
        ("Severity Reason", "severity_reason", None),
        ("Priority", "priority", None),
        ("Priority Reason", "priority_reason", None),
        ("Department", "department", None),
        ("Team", "team", None),
        ("Routing Status", "routing_status", None),
        ("City", "city", None),
        ("District", "district", None),
        ("Area", "area", None),
        ("Estimated Resolution Time", "resolution_time", None),
        ("Estimated Resolution Hours", "resolution_hours", None),
        ("Estimated Resolution Days", "resolution_days", None),
    ]
    for label, key, suffix in display_fields:
        value = result.get(key)
        print(f"\n{label}:" if suffix == "\n" else f"{label}:", value, *([suffix] if suffix else []))

# DUPLICATE RESULT

    print("\n-----------------------------------")
    print("       DUPLICATE DETECTION")
    print("-----------------------------------")

    duplicate = result["duplicate_result"]

    duplicate_fields = [
        ("Duplicate", duplicate, "is_duplicate", None),
        ("Similarity", duplicate, "similarity", "%"),
        ("Existing Complaint ID", duplicate, "existing_complaint_id", None),
        ("Duplicate Message", duplicate, "message", None),
        ("Needs Clarification", result, "needs_clarification", None),
        ("Clarification Question", result, "clarification_question", None),
        ("Reason", result, "reason", None),
        ("Dataset Saved", result, "dataset_saved", None),
    ]
    for label, values, key, suffix in duplicate_fields:
        value = values.get(key) if values else None
        print(label + ":", value, *([suffix] if suffix else []))

# IMAGE RESULT

    if result["image_result"]:

        print("\n-----------------------------------")
        print("          IMAGE ANALYSIS")
        print("-----------------------------------")

        image_fields = [
            ("Image Status", "status"),
            ("Image Valid", "image_valid"),
            ("Image Type", "image_type"),
            ("Image Width", "width"),
            ("Image Height", "height"),
            ("Image Message", "message"),
        ]
        for label, key in image_fields:
            print(label + ":", result["image_result"][key])

# AI RESPONSE

    if result["response"]:

        print("\n-----------------------------------")
        print("          USER RESPONSE")
        print("-----------------------------------")

        print(
            "\n" + result["response"]
        )

    print("\n===================================")
