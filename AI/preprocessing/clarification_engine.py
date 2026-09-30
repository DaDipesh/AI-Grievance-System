# SMART CLARIFICATION ENGINE

from preprocessing.complaint_analyzer import analyze_complaint

# 1. GENERATE CLARIFICATION

def generate_clarification(complaint):

    # Analyze complaint
    result = analyze_complaint(complaint)

    # CASE 1: Actual problem is missing

    if not result["problem_detected"]:

        return {
            "needs_clarification": True,
            "question": (
                "Please describe the actual problem. "
                "For example: water is not coming, "
                "water pressure is low, or water is dirty."
            ),
            "reason": "Actual problem information is missing."
        }

    # CASE 2: Multiple categories detected

    if result["ambiguous"]:

        return {
            "needs_clarification": True,
            "question": (
                "Please describe the main problem "
                "you want to report."
            ),
            "reason": "More than one category detected."
        }

    # CASE 3: Problem is complete

    return {
        "needs_clarification": False,
        "question": None,
        "reason": "Complaint contains sufficient problem information."
    }

# 2. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("     SMART CLARIFICATION ENGINE")
    print("===================================")

    complaint = input(
        "\nEnter complaint: "
    ).strip()

    result = generate_clarification(
        complaint
    )

    print("\n===================================")
    print("       CLARIFICATION RESULT")
    print("===================================")

    print(
        "\nNeeds Clarification:",
        result["needs_clarification"]
    )

    print(
        "Question:",
        result["question"]
    )

    print(
        "Reason:",
        result["reason"]
    )

    print("\n===================================")