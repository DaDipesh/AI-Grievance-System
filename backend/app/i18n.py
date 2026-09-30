MESSAGES = {
    "en": {
        "invalid_mobile": "Enter a valid mobile number.", "unauthorized": "Authentication is required.",
        "forbidden": "You are not authorized to access this resource.", "not_found": "The requested item was not found.",
        "incomplete_complaint": "Describe the problem in at least 10 characters.", "invalid_image": "Upload a valid JPEG, PNG, or WebP image.",
        "location_missing": "Provide a valid complaint location.", "server_error": "Something went wrong. Please try again.",
        "profile_done": "Profile saved successfully.", "registered": "Your complaint {ticket} for {category} in {city}, {area} has been registered.",
        "status": "Your complaint {ticket} status is now {status}.", "resolved": "Your complaint {ticket} has been resolved.",
        "assigned": "New complaint {ticket} is assigned to your department.", "feedback_done": "Thank you for your feedback.",
    },
    "hi": {
        "invalid_mobile": "कृपया मान्य मोबाइल नंबर दर्ज करें।", "unauthorized": "प्रमाणीकरण आवश्यक है।",
        "forbidden": "आपको इस संसाधन को देखने की अनुमति नहीं है।", "not_found": "अनुरोधित जानकारी नहीं मिली।",
        "incomplete_complaint": "समस्या का विवरण कम से कम 10 अक्षरों में दें।", "invalid_image": "मान्य JPEG, PNG या WebP छवि अपलोड करें।",
        "location_missing": "मान्य शिकायत स्थान दर्ज करें।", "server_error": "कुछ गलत हुआ। कृपया फिर से प्रयास करें।",
        "profile_done": "प्रोफ़ाइल सफलतापूर्वक सेव हो गई।", "registered": "आपकी {category} शिकायत, टिकट {ticket}, {city}, {area} के लिए दर्ज हो गई है।",
        "status": "आपकी शिकायत {ticket} की स्थिति अब {status} है।", "resolved": "आपकी शिकायत {ticket} का समाधान हो गया है।",
        "assigned": "नई शिकायत {ticket} आपके विभाग को सौंपी गई है।", "feedback_done": "आपकी प्रतिक्रिया के लिए धन्यवाद।",
    },
}


def message(key: str, language: str = "en", **kwargs) -> str:
    lang = "hi" if str(language).lower().startswith("hi") else "en"
    template = MESSAGES.get(lang, MESSAGES["en"]).get(key, MESSAGES["en"]["server_error"])
    return template.format(**kwargs)


def normalize_ui_language(language: str | None) -> str:
    return "hi" if str(language or "en").lower().startswith("hi") else "en"
