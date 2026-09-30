import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def generate_english_response(category, severity, priority, department, team, duration=None):
    response = (
        "Your complaint has been analyzed successfully.\n\n"
        f"Category: {category}\n"
        f"Severity: {severity}\n"
        f"Priority: {priority}\n"
        f"Assigned Department: {department}\n"
        f"Responsible Team: {team}\n"
    )
    if duration:
        response += f"Reported Duration: {duration}\n"
    return response + "\nYour complaint has been routed to the appropriate department for further action."


def generate_hindi_response(category, severity, priority, department, team, duration=None):
    response = (
        "आपकी शिकायत का सफलतापूर्वक विश्लेषण किया गया है।\n\n"
        f"श्रेणी: {category}\n"
        f"गंभीरता: {severity}\n"
        f"प्राथमिकता: {priority}\n"
        f"संबंधित विभाग: {department}\n"
        f"जिम्मेदार टीम: {team}\n"
    )
    if duration:
        response += f"शिकायत की अवधि: {duration}\n"
    return response + "\nआपकी शिकायत को आगे की कार्रवाई के लिए संबंधित विभाग को भेज दिया गया है।"


def generate_response(language, category, severity, priority, department, team, duration=None):
    normalized_language = (language or "English").strip().casefold()
    if normalized_language in {"hindi", "hinglish"}:
        return generate_hindi_response(category, severity, priority, department, team, duration)
    return generate_english_response(category, severity, priority, department, team, duration)


if __name__ == "__main__":
    language = input("Enter language (English/Hindi/Hinglish): ").strip()
    category = input("Enter category: ").strip()
    severity = input("Enter severity: ").strip()
    priority = input("Enter priority: ").strip()
    department = input("Enter department: ").strip()
    team = input("Enter responsible team: ").strip()
    duration = input("Enter duration (optional): ").strip() or None
    print("\n" + generate_response(language, category, severity, priority, department, team, duration))
