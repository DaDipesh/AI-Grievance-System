import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from language_detector import detect_language

# RESPONSE MESSAGES

responses = {

    "English": {

        "problem":
            "Please describe your actual problem.",

        "location":
            "Please tell us the affected area or locality.",

        "duration":
            "Since when are you facing this problem?"
    },

"Hindi": {

        "problem":
            "कृपया अपनी वास्तविक समस्या के बारे में बताएं।",

        "location":
            "कृपया प्रभावित क्षेत्र या कॉलोनी का नाम बताएं।",

        "duration":
            "यह समस्या कब से है?"
    },

"Hinglish": {

        # Hinglish input ke liye Hindi response

        "problem":
            "कृपया बताएं कि आपकी वास्तविक समस्या क्या है।",

        "location":
            "कृपया प्रभावित क्षेत्र या कॉलोनी का नाम बताएं।",

        "duration":
            "यह समस्या कब से है?"
    }
}

# PROBLEM PATTERNS

problem_patterns = {

# WATER SUPPLY

    "water_supply": [

        # Hinglish
        "pani nahi aa raha",
        "paani nahi aa raha",
        "water nahi aa raha",
        "pani ki supply nahi aa rahi",
        "paani ki supply band hai",

        # English
        "water is not coming",
        "water is not available",
        "no water supply",
        "there is no water supply",
        "water supply is not coming",
        "water supply is not available",

        # Hindi
        "पानी नहीं आ रहा",
        "पानी की सप्लाई नहीं आ रही",
        "पानी की आपूर्ति नहीं हो रही"
    ],

# WATER LEAKAGE

    "water_leakage": [

        # Hinglish
        "pani leak",
        "paani leak",
        "pipeline leak",
        "pipe leak",
        "pani beh raha",
        "paani beh raha hai",

        # English
        "water leakage",
        "water is leaking",
        "pipeline is leaking",
        "pipe is leaking",

        # Hindi
        "पानी लीक हो रहा",
        "पाइपलाइन लीक हो रही"
    ],

# WATERLOGGING

    "waterlogging": [

        # Hinglish
        "road par pani jama",
        "road pe pani jama",
        "sadak par pani jama",
        "road par paani bhara",
        "pani bhar gaya",
        "paani bhar gaya",

        # English
        "water is accumulated on the road",
        "water accumulated on road",
        "waterlogging",
        "road is flooded",
        "water is filled on the road",

        # Hindi
        "सड़क पर पानी जमा",
        "सड़क पर पानी भर गया",
        "सड़क पर जलभराव"
    ],

# DRAINAGE

    "drainage": [

        # Hinglish
        "nali block",
        "nali blocked",
        "nali ka pani",
        "nali me pani jama",
        "nali overflow",
        "drain block",
        "drainage problem",

        # English
        "drain is blocked",
        "drain is overflowing",
        "drainage problem",
        "blocked drain",

        # Hindi
        "नाली बंद",
        "नाली में पानी जमा",
        "नाली ओवरफ्लो",
        "नाली जाम"
    ],

# DIRTY WATER

    "dirty_water": [

        # Hinglish
        "ganda pani",
        "ganda paani",
        "pani ganda aa raha",

        # English
        "dirty water",
        "water is dirty",
        "dirty water supply",
        "contaminated water",

        # Hindi
        "गंदा पानी",
        "पानी गंदा आ रहा है",
        "दूषित पानी"
    ],

# ELECTRICITY
    "electricity": [

    # Hinglish

    "bijli nahi aa rahi",
    "bijli nahi hai",
    "bijli nahi aati",
    "bijli band hai",
    "bijli chali gayi",
    "bijli ja rahi",
    "bijli baar baar ja rahi",
    "bijli baar baar jaati hai",
    "light nahi aa rahi",
    "light nahi hai",
    "light band hai",
    "power cut",

    # English

    "electricity is not available",
    "electricity is not coming",
    "no electricity",
    "there is no electricity",
    "power is out",
    "power cut",
    "electricity is gone",

    # Hindi

    "बिजली नहीं आ रही",
    "बिजली नहीं है",
    "बिजली नहीं आती",
    "बिजली बंद है",
    "बिजली चली गई",
    "बिजली जा रही है",
    "बिजली बार बार जा रही है"
    ],

    # STREET LIGHT

    "street_light": [

        # Hinglish
        "street light band",
        "street light kharab",
        "gali ki light band",

        # English
        "street light is not working",
        "street light is broken",
        "street light not working",

        # Hindi
        "स्ट्रीट लाइट बंद",
        "स्ट्रीट लाइट खराब"
    ],

# ROAD

    "road": [

        # Hinglish
        "road kharab",
        "sadak kharab",
        "road me gaddha",
        "sadak me gaddha",
        "pothole",

        # English
        "road is damaged",
        "road is broken",
        "potholes on road",
        "road has potholes",

        # Hindi
        "सड़क खराब",
        "सड़क में गड्ढा",
        "सड़क टूटी हुई है"
    ],

# GARBAGE

    "garbage": [

        # Hinglish
        "kachra nahi uth raha",
        "kachra jama",
        "garbage collect nahi ho raha",
        "dustbin bhara",

        # English
        "garbage is not collected",
        "garbage is not being collected",
        "garbage is accumulated",
        "dustbin is full",

        # Hindi
        "कचरा नहीं उठ रहा",
        "कचरा जमा है",
        "कूड़ेदान भरा है"
    ]
}

# ANALYZE COMPLAINT

def analyze_complaint(complaint):

    text = complaint.strip().lower()

    result = {

        "problem_type": None,

        "location": None,

        "duration": None
    }

# PROBLEM DETECTION

    for problem_type, patterns in problem_patterns.items():

        for pattern in patterns:

            if pattern in text:

                result["problem_type"] = problem_type

                break

        if result["problem_type"]:

            break

# LOCATION DETECTION

    location_words = [

        "ratibad",
        "bhopal",
        "indore",
        "shiv nagar",

        "area",
        "colony",
        "nagar",
        "mohalla",
        "gali",
        "street",

        "क्षेत्र",
        "कॉलोनी",
        "नगर",
        "मोहल्ला",
        "गली"
    ]

    for word in location_words:

        if word in text:

            result["location"] = word

            break

# DURATION DETECTION

    duration_words = [

        "since",
        "for",
        "days",
        "day",
        "hours",
        "hour",
        "week",
        "weeks",

        "din",
        "ghante",
        "hafta",
        "mahine",
        "kal",
        "aaj",

        "दिन",
        "घंटे",
        "हफ्ते",
        "महीने"
    ]

    for word in duration_words:

        if word in text:

            result["duration"] = word

            break

    return result

# AI GRIEVANCE ASSISTANT
print("\n===================================")
print("       AI GRIEVANCE ASSISTANT")
print("===================================")

complaint = input("\nEnter your complaint: ")
input_language = detect_language(complaint)
print("\nDetected Language:", input_language)

if input_language == "Hinglish":
    response_language = "Hinglish"
else:
    response_language = input_language

conversation = {
    "input_language": input_language,
    "response_language": response_language,
    "complaint": complaint,
    "problem_type": None,
    "location": None,
    "duration": None,
}

while True:
    result = analyze_complaint(conversation["complaint"])
    conversation["problem_type"] = result["problem_type"]
    conversation["location"] = result["location"]
    conversation["duration"] = result["duration"]

    if conversation["problem_type"] is None:
        print("\nðŸ¤–", responses[response_language]["problem"])
        answer = input("> ")
        conversation["complaint"] += " " + answer
        continue

    if conversation["location"] is None:
        print("\nðŸ¤–", responses[response_language]["location"])
        answer = input("> ").strip()
        conversation["location"] = answer
        conversation["complaint"] += " " + answer
        continue

    if conversation["duration"] is None:
        print("\nðŸ¤–", responses[response_language]["duration"])
        answer = input("> ").strip()
        conversation["duration"] = answer
        conversation["complaint"] += " " + answer
        continue

    print("\n===================================")
    print("   âœ… COMPLAINT INFORMATION COMPLETE")
    print("===================================")
    print("Problem      :", conversation["problem_type"])
    print("Location     :", conversation["location"])
    print("Duration     :", conversation["duration"])
    print("Input Language :", conversation["input_language"])
    if conversation["input_language"] == "Hinglish":
        print("Response Language : Hindi")
    else:
        print("Response Language :", conversation["response_language"])
    print("\nFinal Complaint:")
    print(conversation["complaint"])
    print("\n===================================")
    break
