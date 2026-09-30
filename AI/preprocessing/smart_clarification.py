try:
    from .language_detector import detect_language
except ImportError:
    from language_detector import detect_language
import joblib
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AI_DIR = Path(__file__).resolve().parents[1]

# LOAD ML MODEL

model = joblib.load(AI_DIR / "models" / "trained_model.pkl")
vectorizer = joblib.load(AI_DIR / "models" / "vectorizer.pkl")

# 8 CATEGORIES

categories = [
    "Water Supply",
    "Electricity",
    "Street Light",
    "Road",
    "Healthcare",
    "Sanitation",
    "Drainage",
    "Environment"
]

# CATEGORY KEYWORDS
# Used only to detect incomplete complaints

category_words = {

    "Water Supply": [
        "water",
        "pani",
        "paani",
        "पानी"
    ],

    "Electricity": [
        "electricity",
        "bijli",
        "light",
        "power",
        "बिजली"
    ],

    "Street Light": [
        "street light",
        "streetlight",
        "gali ki light",
        "स्ट्रीट लाइट"
    ],

    "Road": [
        "road",
        "sadak",
        "सड़क"
    ],

    "Healthcare": [
        "hospital",
        "doctor",
        "medicine",
        "health",
        "अस्पताल",
        "डॉक्टर",
        "दवा"
    ],

    "Sanitation": [
        "garbage",
        "kachra",
        "safai",
        "dustbin",
        "कचरा",
        "सफाई",
        "कूड़ा"
    ],

    "Drainage": [
        "drain",
        "drainage",
        "nali",
        "नाली",
        "ड्रेनेज"
    ],

    "Environment": [
        "environment",
        "pollution",
        "smoke",
        "tree",
        "पर्यावरण",
        "प्रदूषण",
        "धुआं",
        "पेड़"
    ]
}

# QUESTIONS WHEN PROBLEM IS MISSING

problem_questions = {

    "English": {

        "Water Supply":
            "What is the actual water-related problem?",

        "Electricity":
            "What is the actual electricity-related problem?",

        "Street Light":
            "What is the actual street light problem?",

        "Road":
            "What is the actual road problem?",

        "Healthcare":
            "What is the actual healthcare-related problem?",

        "Sanitation":
            "What is the actual sanitation problem?",

        "Drainage":
            "What is the actual drainage problem?",

        "Environment":
            "What is the actual environmental problem?"
    },

"Hindi": {

        "Water Supply":
            "पानी से संबंधित आपकी वास्तविक समस्या क्या है?",

        "Electricity":
            "बिजली से संबंधित आपकी वास्तविक समस्या क्या है?",

        "Street Light":
            "स्ट्रीट लाइट से संबंधित आपकी वास्तविक समस्या क्या है?",

        "Road":
            "सड़क से संबंधित आपकी वास्तविक समस्या क्या है?",

        "Healthcare":
            "स्वास्थ्य से संबंधित आपकी वास्तविक समस्या क्या है?",

        "Sanitation":
            "सफाई से संबंधित आपकी वास्तविक समस्या क्या है?",

        "Drainage":
            "ड्रेनेज से संबंधित आपकी वास्तविक समस्या क्या है?",

        "Environment":
            "पर्यावरण से संबंधित आपकी वास्तविक समस्या क्या है?"
    }
}

# LOW CONFIDENCE QUESTIONS

clarification_questions = {

    "English": {

        "Water Supply":
            "Is the water supply unavailable, is the pressure low, or is there another issue?",

        "Electricity":
            "Is the power supply off, is there a voltage issue, or are there frequent power cuts?",

        "Street Light":
            "Is the street light not working, damaged, or switching off frequently?",

        "Road":
            "Are there potholes, is the road damaged, or is there another issue?",

        "Healthcare":
            "Is the problem related to a doctor, medicine, ambulance, or hospital facility?",

        "Sanitation":
            "Is garbage not being collected, is the dustbin full, or is the area not being cleaned?",

        "Drainage":
            "Is the drain blocked, overflowing, or is there a wastewater problem?",

        "Environment":
            "Is the problem related to pollution, smoke, garbage burning, or environmental damage?"
    },

"Hindi": {

        "Water Supply":
            "क्या पानी की सप्लाई बंद है, पानी का दबाव कम है या कोई दूसरी समस्या है?",

        "Electricity":
            "क्या बिजली की सप्लाई बंद है, वोल्टेज की समस्या है या बार-बार बिजली जा रही है?",

        "Street Light":
            "क्या स्ट्रीट लाइट बंद है, खराब है या बार-बार बंद हो रही है?",

        "Road":
            "क्या सड़क में गड्ढे हैं, सड़क टूटी हुई है या कोई दूसरी समस्या है?",

        "Healthcare":
            "क्या समस्या डॉक्टर, दवा, एम्बुलेंस या अस्पताल की सुविधा से संबंधित है?",

        "Sanitation":
            "क्या कचरा नहीं उठ रहा है, कूड़ेदान भरा है या इलाके की सफाई नहीं हो रही है?",

        "Drainage":
            "क्या नाली बंद है, ओवरफ्लो हो रही है या गंदे पानी की समस्या है?",

        "Environment":
            "क्या समस्या प्रदूषण, धुआं, कचरा जलाने या पर्यावरण को नुकसान से संबंधित है?"
    }
}

# DETECT CATEGORY TOPIC

def detect_topic(text):

    text = text.lower()

    for category, words in category_words.items():

        for word in words:

            if word in text:

                return category

    return None

# CHECK IF COMPLAINT IS TOO SHORT

def is_incomplete(text):

    words = text.strip().split()

    # Very short input
    if len(words) <= 3:
        return True

    return False

# GET LANGUAGE FOR RESPONSE

def get_response_language(language):

    if language == "Hinglish":
        return "Hindi"

    return language

# ML PREDICTION

def predict_category(complaint):

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

# MAIN PROGRAM

print("\n===================================")
print("       AI GRIEVANCE ASSISTANT")
print("===================================")

# STEP 1 — USER ENTERS PROBLEM

complaint = input(
    "\nEnter your complaint: "
).strip()

# STEP 2 — LANGUAGE DETECTION

input_language = detect_language(
    complaint
)

response_language = get_response_language(
    input_language
)

print(
    "\nDetected Language:",
    input_language
)

print(
    "Response Language:",
    response_language
)

# STEP 3 — CHECK INCOMPLETE COMPLAINT

topic = detect_topic(complaint)

if is_incomplete(complaint) and topic is not None:

    print("\n🤖", problem_questions[response_language][topic])

    answer = input("> ").strip()

    complaint = complaint + " " + answer

# STEP 4 — RUN ML MODEL

prediction, confidence = predict_category(
    complaint
)

print("\n===================================")
print("AI ANALYSIS")
print("===================================")

print("\nComplaint:")
print(complaint)

print("\nPredicted Category:")
print(prediction)

print("\nConfidence:")
print(round(confidence, 2), "%")

# STEP 5 — LOW CONFIDENCE

if confidence < 50:

    print("\n🤖", clarification_questions[response_language][prediction])

    answer = input("> ").strip()

    complaint = complaint + " " + answer

    # Re-analyze after clarification

    prediction, confidence = predict_category(
        complaint
    )

    print("\n===================================")
    print("UPDATED AI ANALYSIS")
    print("===================================")

    print("\nFinal Complaint:")
    print(complaint)

    print("\nFinal Category:")
    print(prediction)

    print("\nNew Confidence:")
    print(round(confidence, 2), "%")

else:

    print("\n✅ Complaint understood by AI.")

print("\n===================================")
