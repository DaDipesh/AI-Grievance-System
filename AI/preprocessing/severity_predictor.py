# SEVERITY PREDICTOR

import re

# 1. CRITICAL KEYWORDS

critical_keywords = [

    # Healthcare / Emergency
    "emergency",
    "ambulance",
    "life threatening",
    "serious injury",
    "critical patient",
    "patient emergency",
    "आपातकाल",
    "एम्बुलेंस",
    "गंभीर मरीज",
    "गंभीर चोट",

    # Electricity danger
    "electric shock",
    "sparking",
    "live wire",
    "electric wire fallen",
    "wire hanging",
    "बिजली का झटका",
    "चिंगारी",
    "खुला तार",
    "बिजली का तार गिरा",

    # Major environmental danger
    "toxic smoke",
    "chemical leak",
    "gas leak",
    "poisonous gas",
    "जहरीला धुआं",
    "गैस रिसाव",
    "रासायनिक रिसाव"
]

# 2. HIGH SEVERITY KEYWORDS

high_keywords = [

    # Water
    "no water",
    "water not coming",
    "pani nahi aa raha",
    "पानी नहीं आ रहा",

    # Electricity
    "power outage",
    "power cut",
    "bijli nahi",
    "बिजली नहीं",

    # Road
    "large pothole",
    "big pothole",
    "major road damage",
    "bada gaddha",
    "bahut bada gaddha",
    "बड़ा गड्ढा",
    "बहुत बड़ा गड्ढा",

    # Drainage
    "major waterlogging",
    "severe waterlogging",
    "drain overflow",
    "nali overflow",
    "बहुत ज्यादा जलभराव",
    "नाली ओवरफ्लो",

    # Sanitation
    "garbage accumulated",
    "large garbage pile",
    "बहुत कचरा जमा",

    # Environment
    "heavy pollution",
    "severe pollution",
    "खुले में प्लास्टिक जला",
    "प्लास्टिक जलाने से धुआँ",
    "खुले में कचरा जला",
    "कचरा जलाने से धुआँ",
    "बहुत ज्यादा प्रदूषण"
]

# 3. MEDIUM SEVERITY KEYWORDS

medium_keywords = [

    "low water pressure",
    "pani kam aa raha",
    "पानी कम आ रहा",

    "street light",
    "streetlight",
    "street light band",
    "street light kharab",
    "स्ट्रीट लाइट बंद",
    "स्ट्रीट लाइट खराब",

    "road damaged",
    "road kharab",
    "road damage",
    "सड़क खराब",

    "garbage",
    "kachra",
    "कचरा",

    "dustbin full",
    "dustbin bhara",
    "कूड़ेदान भरा",

    "drainage problem",
    "nali blocked",
    "nali block",
    "नाली बंद",
    "नाली ब्लॉक",

    "pollution",
    "प्रदूषण"
]

# 4. DURATION DETECTION

def detect_duration_days(text):

    text_lower = text.lower()

    # Numeric days
    match = re.search(
        r"\b(\d+)\s*(day|days|din|dino|दिन)\b",
        text_lower
    )

    if match:
        return int(match.group(1))

    # Numeric weeks
    match = re.search(
        r"\b(\d+)\s*(week|weeks|hafta|hafte|हफ्ता|हफ्ते)\b",
        text_lower
    )

    if match:
        return int(match.group(1)) * 7

    # Numeric months
    match = re.search(
        r"\b(\d+)\s*(month|months|mahina|mahine|महीना|महीने)\b",
        text_lower
    )

    if match:
        return int(match.group(1)) * 30

    # Yesterday / yesterday onwards
    if "kal se" in text_lower:
        return 1

    if "since yesterday" in text_lower:
        return 1

    return 0

# 5. KEYWORD CHECK

def contains_keyword(text, keywords):

    text_lower = text.lower()

    for keyword in keywords:

        if keyword.lower() in text_lower:
            return True

    return False

# 6. SEVERITY PREDICTION

def predict_severity(
    complaint,
    category=None
):

    text_lower = complaint.lower()

    # Step 1: Critical

    if contains_keyword(
        text_lower,
        critical_keywords
    ):

        return {
            "severity": "Critical",
            "reason": "Critical safety or emergency issue detected."
        }

# Step 2: Duration

    duration_days = detect_duration_days(
        complaint
    )

# Step 3: High severity

    if contains_keyword(
        text_lower,
        high_keywords
    ):

        return {
            "severity": "High",
            "reason": "High-impact problem detected."
        }

# Long duration increases severity

    if duration_days >= 7:

        return {
            "severity": "High",
            "reason": "Complaint has continued for 7 or more days."
        }

# Step 4: Medium severity

    if contains_keyword(
        text_lower,
        medium_keywords
    ):

        return {
            "severity": "Medium",
            "reason": "Moderate public-service issue detected."
        }

# Duration of 3+ days

    if duration_days >= 3:

        return {
            "severity": "Medium",
            "reason": "Complaint has continued for several days."
        }

    # A confirmed service problem should not be labeled Low just because its
    # wording misses a severity keyword. Category-specific urgency rules above
    # still take precedence (for example, exposed wires are Critical).
    if category in {
        "Water Supply", "Electricity", "Street Light", "Road",
        "Healthcare", "Sanitation", "Drainage", "Environment",
    }:
        return {
            "severity": "Medium",
            "reason": "A confirmed public-service problem requires timely attention.",
        }

# Step 5: Default

    return {
        "severity": "Low",
        "reason": "No high-impact or emergency indicator detected."
    }

# 7. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("       SEVERITY PREDICTOR")
    print("===================================")

    complaint = input(
        "\nEnter complaint: "
    ).strip()

    result = predict_severity(
        complaint
    )

    print("\n===================================")
    print("        SEVERITY RESULT")
    print("===================================")

    print(
        "\nSeverity:",
        result["severity"]
    )

    print(
        "Reason:",
        result["reason"]
    )

    print("\n===================================")
