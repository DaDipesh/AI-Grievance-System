# PRIORITY ENGINE

import re

# 1. DURATION DETECTOR

def detect_duration_days(complaint):

    text = complaint.lower()

    if re.search(r"\b(several|a few|few)\s+days\b", text):
        return 3

    # "kal se"

    if "kal se" in text or "since yesterday" in text:
        return 1

    # Days

    day_match = re.search(
        r"(\d+)\s*(day|days|din)",
        text
    )

    if day_match:
        return int(day_match.group(1))

    # Weeks

    week_match = re.search(
        r"(\d+)\s*(week|weeks|hafte|hafta)",
        text
    )

    if week_match:
        return int(week_match.group(1)) * 7

    # Months

    month_match = re.search(
        r"(\d+)\s*(month|months|mahine|mahina)",
        text
    )

    if month_match:
        return int(month_match.group(1)) * 30

    return 0

# 2. PRIORITY PREDICTION

def predict_priority(
    complaint,
    severity,
    category=None
    ):

    duration_days = detect_duration_days(
        complaint
    )

# URGENT PRIORITY

    if severity == "Critical":

        priority = "Urgent"

        reason = (
            "Critical issue requires immediate attention."
        )

# HIGH PRIORITY

    elif severity == "High":

        priority = "High"

        reason = (
            "High severity complaint requires "
            "early resolution."
        )

# LONG PENDING COMPLAINT

    elif duration_days >= 7:

        priority = "High"

        reason = (
            "Complaint has remained unresolved "
            "for a long duration."
        )

# MEDIUM PRIORITY

    elif severity == "Medium":

        priority = "Medium"

        reason = (
            "Complaint requires timely attention."
        )

# DEFAULT

    else:

        priority = "Normal"

        reason = (
            "Complaint does not indicate "
            "immediate urgency."
        )

# RESULT

    return {

        "priority":
            priority,

        "priority_reason":
            reason,

        "duration_days":
            duration_days,

        "severity":
            severity,

        "category":
            category
    }

# 3. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("        PRIORITY ENGINE")
    print("===================================")

    complaint = input(
        "\nEnter complaint: "
    ).strip()

    severity = input(
        "Enter severity "
        "(Low/Medium/High/Critical): "
    ).strip()

    category = input(
        "Enter category: "
    ).strip()

    result = predict_priority(
        complaint,
        severity,
        category
    )

    print("\n===================================")
    print("          PRIORITY RESULT")
    print("===================================")

    print(
        "\nPriority:",
        result["priority"]
    )

    print(
        "Priority Reason:",
        result["priority_reason"]
    )

    print(
        "Duration (Days):",
        result["duration_days"]
    )

    print(
        "Severity:",
        result["severity"]
    )

    print(
        "Category:",
        result["category"]
    )

    print("\n===================================")
