# COMPLAINT ANALYZER

import re

# 1. PROBLEM PATTERNS - 8 CATEGORIES

# 1. PROBLEM PATTERNS - 8 CATEGORIES

problem_patterns = {

    # WATER SUPPLY

    "Water Supply": [

        # Hinglish
        "pani nahi aa raha",
        "paani nahi aa raha",
        "pani kam aa raha",
        "paani kam aa raha",
        "pani ki supply nahi",
        "paani ki supply nahi",
        "water nahi aa raha",
        "water supply nahi",
        "pani ganda aa raha",
        "paani ganda aa raha",
        "pani dirty hai",
        "water pressure low",
        "pani ka pressure low",
        "pani ka pressure kam",
        "nal me pani nahi aa raha",

        # English
        "water is not coming",
        "water is not available",
        "no water supply",
        "there is no water",
        "water supply is not available",
        "water supply stopped",
        "water supply has stopped",
        "water pressure is low",
        "low water pressure",
        "water is dirty",
        "dirty water",
        "water is contaminated",

        # Hindi
        "पानी नहीं आ रहा",
        "पानी कम आ रहा",
        "पानी की सप्लाई नहीं",
        "पानी गंदा आ रहा",
        "पानी गंदा है",
        "पानी का दबाव कम",
        "पानी का प्रेशर कम",
        "नल में पानी नहीं आ रहा",
        "जल आपूर्ति नहीं",
        "जल आपूर्ति बंद"
    ],

# ELECTRICITY

    "Electricity": [

        # Hinglish
        "bijli nahi aa rahi",
        "bijli nahi hai",
        "bijli band hai",
        "bijli chali gayi",
        "bijli ja rahi",
        "bijli baar baar ja rahi",
        "light nahi aa rahi",
        "light chali gayi",
        "power cut",
        "voltage kam",
        "voltage problem",
        "bijli ka problem",
        "electricity problem",

        # English
        "electricity is not available",
        "electricity is not coming",
        "there is no electricity",
        "power is out",
        "power outage",
        "power cut",
        "electricity supply stopped",
        "low voltage",
        "voltage problem",
        "frequent power cuts",

        # Hindi
        "बिजली नहीं आ रही",
        "बिजली नहीं है",
        "बिजली बंद है",
        "बिजली चली गई",
        "बिजली बार बार जा रही",
        "लाइट नहीं आ रही",
        "पावर कट",
        "वोल्टेज कम",
        "वोल्टेज की समस्या",
        "बिजली की समस्या"
    ],

# STREET LIGHT

    "Street Light": [

        # Hinglish
        "street light band",
        "street light kharab",
        "street light nahi jal",
        "streetlight band",
        "streetlight kharab",
        "gali ki light band",
        "gali ki light kharab",
        "gali ki street light band",
        "road ki light band",
        "light nahi jal rahi",
        "street light not working",

        # English
        "street light is not working",
        "streetlight is not working",
        "street light is broken",
        "street light is damaged",
        "street light is off",
        "road light is not working",
        "street lighting problem",

        # Hindi
        "स्ट्रीट लाइट बंद",
        "स्ट्रीट लाइट खराब",
        "स्ट्रीट लाइट नहीं जल रही",
        "गली की लाइट बंद",
        "गली की लाइट खराब",
        "सड़क की लाइट बंद",
        "स्ट्रीट लाइट काम नहीं कर रही"
    ],

# ROAD

    "Road": [

        # Hinglish
        "road kharab",
        "road me gaddha",
        "road par gaddha",
        "road toot gayi",
        "road toot",
        "road damaged",
        "broken road",
        "road damage",
        "sadak kharab",
        "sadak me gaddha",
        "sadak par gaddha",
        "sadak toot",
        "bada gaddha",
        "road me bahut bada gaddha",
        "pothole",

        # English
        "road is damaged",
        "road is broken",
        "broken road",
        "damaged road",
        "road has potholes",
        "there is a pothole",
        "large pothole",
        "big pothole",
        "road damage",
        "road condition is bad",

        # Hindi
        "सड़क खराब",
        "सड़क में गड्ढा",
        "सड़क पर गड्ढा",
        "सड़क टूटी",
        "सड़क टूट गई",
        "बड़ा गड्ढा",
        "सड़क में बहुत बड़ा गड्ढा",
        "सड़क क्षतिग्रस्त",
        "सड़क की हालत खराब",
        "गड्ढा"
    ],

# HEALTHCARE

    "Healthcare": [

        # Hinglish
        "doctor nahi",
        "doctor nahi hai",
        "doctor available nahi",
        "doctor available nahi hai",
        "medicine nahi",
        "medicine nahi hai",
        "medicine available nahi",
        "dawai nahi",
        "dawai nahi hai",
        "ambulance nahi",
        "ambulance available nahi",
        "hospital me problem",
        "hospital ki facility nahi",
        "health centre problem",
        "health center problem",

        # English
        "doctor is not available",
        "doctor not available",
        "no doctor available",
        "medicine is not available",
        "medicines are not available",
        "no medicine available",
        "ambulance is not available",
        "no ambulance available",
        "hospital problem",
        "hospital facility problem",
        "health center problem",
        "healthcare facility problem",

        # Hindi
        "डॉक्टर नहीं",
        "डॉक्टर उपलब्ध नहीं",
        "डॉक्टर उपलब्ध नहीं है",
        "दवा नहीं",
        "दवाई नहीं",
        "दवा उपलब्ध नहीं",
        "दवाई उपलब्ध नहीं",
        "एम्बुलेंस नहीं",
        "एम्बुलेंस उपलब्ध नहीं",
        "अस्पताल में समस्या",
        "अस्पताल की सुविधा नहीं",
        "स्वास्थ्य केंद्र की समस्या"
    ],

# SANITATION

    "Sanitation": [

        # Hinglish
        "kachra nahi uth",
        "kachra nahi uth raha",
        "kachra jama",
        "kachra pada hai",
        "garbage nahi uth",
        "garbage nahi uth raha",
        "garbage collection nahi",
        "dustbin full",
        "dustbin bhara",
        "safai nahi",
        "area ki safai nahi",
        "garbage jama",
        "kachra bahut hai",
        "safai ka problem",

        # English
        "garbage is not collected",
        "garbage collection is not happening",
        "garbage is lying around",
        "garbage has accumulated",
        "garbage bin is full",
        "garbage bin has been full",
        "garbage bin is overflowing",
        "garbage bin has been overflowing",
        "dustbin is full",
        "dustbin is overflowing",
        "cleaning is not happening",
        "area is not clean",
        "sanitation problem",
        "waste collection problem",

        # Hindi
        "कचरा नहीं उठ रहा",
        "कचरा जमा है",
        "कचरा पड़ा है",
        "कचरा बहुत है",
        "कूड़ेदान भरा है",
        "कूड़ेदान भर गया",
        "सफाई नहीं हो रही",
        "इलाके में सफाई नहीं",
        "कचरा जमा हो गया",
        "सफाई की समस्या"
    ],

# DRAINAGE

    "Drainage": [

        # Hinglish
        "nali block",
        "nali blocked",
        "nali band",
        "nali overflow",
        "nali ka pani",
        "nali me pani",
        "nali ka pani road par",
        "drain block",
        "drain blocked",
        "drainage problem",
        "drain overflow",
        "wastewater",
        "pani jama",
        "paani jama",
        "water jama",
        "waterlogging",
        "pani bhara",
        "paani bhara",
        "road par pani jama",
        "road par paani jama",
        "road me pani jama",
        "road me paani jama",

        # English
        "drain is blocked",
        "drain is clogged",
        "drainage is blocked",
        "blocked drain",
        "drain overflow",
        "drain is overflowing",
        "drainage problem",
        "waterlogging",
        "water is accumulated",
        "water has accumulated",
        "water is stagnant",
        "wastewater is flowing",
        "water accumulated on road",

        # Hindi
        "नाली बंद",
        "नाली ब्लॉक",
        "नाली जाम",
        "नाली ओवरफ्लो",
        "नाली में पानी",
        "नाली का पानी",
        "नाली का पानी सड़क पर",
        "ड्रेनेज की समस्या",
        "नाली की समस्या",
        "पानी जमा",
        "पानी भरा",
        "जलभराव",
        "सड़क पर पानी जमा",
        "सड़क पर पानी भरा"
    ],

# ENVIRONMENT

    "Environment": [

        # Hinglish
        "pollution",
        "air pollution",
        "smoke",
        "dhua",
        "dhua aa raha",
        "dhua bahut hai",
        "kachra jala",
        "kachra jal raha",
        "garbage burning",
        "tree cut",
        "ped kaat",
        "ped kaat rahe",
        "environment problem",
        "hawa polluted hai",

        # English
        "air pollution",
        "environment pollution",
        "pollution problem",
        "smoke pollution",
        "smoke is coming",
        "garbage is being burned",
        "garbage burning",
        "trees are being cut",
        "tree cutting",
        "environmental problem",
        "air quality problem",

        # Hindi
        "प्रदूषण",
        "वायु प्रदूषण",
        "धुआं",
        "धुआं आ रहा",
        "बहुत धुआं है",
        "कचरा जल रहा",
        "कचरा जलाना",
        "पेड़ काट रहे",
        "पेड़ काटना",
        "पर्यावरण की समस्या",
        "हवा प्रदूषित है"
    ]
}

# Fallback issue signals for common wording that is not covered by the exact
# examples above. Each category requires a problem phrase; this avoids treating
# a bare location or service name as a complete complaint. Hindi signals are
# kept as real Unicode text so they work with UTF-8 complaint input.
category_issue_signals = {
    "Water Supply": {
        "subjects": ("water", "pani", "paani", "पानी", "जल"),
        "issues": (
            "no water", "not coming", "not available", "irregular",
            "shortage", "low pressure", "pressure is low", "dirty",
            "contaminated", "supply stopped", "supply is stopped",
            "kam", "low", "very little", "supply nahi", "not reaching", "only for",
            "few minutes", "minutes every day", "not supplying", "nahi aaya", "nahi aa",
            "band", "aa raha", "आ रहा", "कम", "बहुत कम", "कम दबाव",
            "sirf kuch minute", "केवल कुछ मिनट",
            "नहीं आ", "नहीं मिल", "अनियमित", "कम दबाव", "दबाव कम",
            "गंदा", "दूषित", "आपूर्ति बंद", "जलापूर्ति बंद", "बंद",
        ),
    },
    "Electricity": {
        "subjects": ("electricity", "electric", "power", "voltage", "light", "bijli", "बिजली", "transformer", "ट्रांसफॉर्मर", "wire", "cable", "electric pole", "electrical pole"),
        "issues": (
            "no electricity", "power cut", "power outage", "outage",
            "not available", "supply stopped", "interrupted", "low voltage",
            "voltage fluctuates", "voltage fluctuation", "problem",
            "low", "fluctuate", "goes off", "suddenly stopped", "cut",
            "chali ja", "ja rahi", "band ho", "band", "light chali", "चली जा", "कम", "कम-ज्यादा", "जा रही",
            "नहीं है", "बंद", "कटौती", "कम वोल्टेज", "वोल्टेज कम",
            "उतार-चढ़ाव", "खराबी", "समस्या", "fallen", "hanging", "sparking", "spark", "shock", "exposed", "broken", "damaged",
        ),
    },
    "Street Light": {
        "subjects": ("street light", "streetlight", "road light", "gali ki light", "street lighting", "streetlight", "light", "रोशनी", "लाइट", "स्ट्रीट लाइट", "गली की लाइट", "सड़क की लाइट"),
        "issues": (
            "not working", "not lighting", "keeps switching off", "switching off",
            "is off", "broken", "damaged", "dark", "band", "kharab",
            "nahi jal", "blink", "lighting", "poor", "kam", "pole damage",
            "remains dark", "बिना permission", "नहीं जल", "बंद", "खराब",
            "क्षतिग्रस्त", "अंधेरा", "कम", "नहीं जलती",
        ),
    },
    "Road": {
        "subjects": ("road", "roads", "sadak", "pothole", "gaddha", "gaddhe", "gaddhon", "गड्ढा", "गड्ढे", "गड्ढों", "सड़क", "सड़क"),
        "issues": (
            "pothole", "gaddha", "gaddhe", "damaged", "damage", "broken",
            "crack", "cracks", "repair", "kharab", "toot", "गड्ढा", "गड्ढे",
            "खराब", "टूट", "दरार", "मरम्मत", "क्षतिग्रस्त",
            "uneven", "unsafe", "risk", "accident", "mushkil", "difficult",
            "चलाना मुश्किल", "असमान", "दुर्घटना", "खतरा", "मुश्किल",
        ),
    },
    "Healthcare": {
        "subjects": ("doctor", "medicine", "medicines", "dawai", "ambulance", "hospital", "health center", "health centre", "डॉक्टर", "दवा", "दवाई", "एम्बुलेंस", "अस्पताल", "स्वास्थ्य केंद्र"),
        "issues": (
            "no ", "not available", "unavailable", "shortage", "lack of",
            "problem", "facility", "नहीं", "अनुपलब्ध", "कमी", "समस्या", "सुविधा",
            "insufficient", "lack", "not arriving", "on time", "waiting",
            "wait", "staff", "beds", "essential", "basic", "mil rahi",
            "nahi mil", "nahi hain", "nahi hai", "kam", "bahut der", "नहीं मिल", "इंतजार", "प्रतीक्षा",
            "पर्याप्त", "कम", "कमी",
        ),
    },
    "Sanitation": {
        "subjects": ("garbage", "trash", "waste", "dustbin", "garbage bin", "bin", "kachra", "kooda", "safai", "sanitation worker", "cleaning", "street", "कचरा", "कूड़ा", "कूड़ादान", "कूड़ेदान", "सफाई", "सफाई कर्मचारी"),
        "issues": (
            "full", "overflow", "not collected", "collection", "accumulated",
            "lying around", "lying in", "not picked", "dirty", "jama", "bhara", "नहीं उठा",
            "नहीं उठाया", "जमा", "भरा", "ओवरफ्लो", "सड़", "गंदगी",
            "not being collected", "not coming", "regular", "dumped", "thrown",
            "not cleaned", "has not been cleaned", "collection", "pada hua", "nahi aa", "nahi hui",
            "nahi ho", "bhar", "bahar aa", "phenka ja", "डाला", "फेंका", "नहीं हुआ",
            "नहीं हुई", "नियमित", "बाहर आ", "पड़ा", "has not been collected", "has not been picked up", "not picked up", "uncollected",
        ),
    },
    "Drainage": {
        "subjects": ("drain", "drainage", "nali", "नाली", "sewer", "sewage", "waterlogging", "water logging", "जलभराव"),
        "issues": (
            "blocked", "blockage", "clogged", "overflow", "overflowing",
            "stagnant", "water is accumulated", "water has accumulated",
            "जाम", "बंद", "भर", "ओवरफ्लो", "रुका", "जमा",
            "water is stagnant", "water has accumulated", "water accumulated",
            "sewer", "sewage", "water on road", "भराव", "बह रहा", "गंदा पानी",
        ),
    },
    "Environment": {
        "subjects": ("pollution", "polluted", "smoke", "garbage", "plastic", "धुआँ", "धुआं", "प्रदूषण", "air quality", "tree", "trees", "ped", "पेड़", "पेड़", "कचरा", "प्लास्टिक"),
        "issues": (
            "problem", "heavy", "bad", "burning", "burned", "cutting", "cut down",
            "जल", "जला", "काट", "खराब", "बहुत", "समस्या",
            "burning", "burned", "burn", "cut", "cutting", "removed",
            "jala", "jal rahe", "kaate", "kaat", "धुआँ", "धुआं", "जला रहे",
        ),
    },
}

# 2. DURATION PATTERNS

duration_patterns = [

    # English
    r"\b\d+\s+(day|days|hour|hours|week|weeks|month|months)\b",

    # Hinglish
    r"\b\d+\s+(din|dino|ghanta|ghante|hafta|hafte|mahina|mahine)\b",

    # Hindi
    r"\b\d+\s+(दिन|घंटा|घंटे|हफ्ता|हफ्ते|महीना|महीने)\b",

    # Common expressions
    r"\b(several|a few|few)\s+days\b",
    r"\b(kal se|aaj se)\b",
    r"\b(since yesterday|since today)\b",

    # English: since Monday etc.
    r"\bsince\s+\w+",

    # English: for 3 days
    r"\bfor\s+\d+\s+\w+"
]

# 3. DETECT PROBLEM

def detect_problem(text):

    if not isinstance(text, str) or not text.strip():
        return []

    text_lower = text.casefold()

    found = []

    for category, patterns in problem_patterns.items():

        for pattern in patterns:

            if pattern in text_lower:

                # STREET LIGHT TOPIC ALONE
                # is NOT an actual problem

                if category == "Street Light":

                    problem_words = [

                        "band",
                        "kharab",
                        "nahi",
                        "not working",
                        "broken",
                        "damage",
                        "damaged",
                        "off",

                        "खराब",
                        "बंद",
                        "नहीं",
                        "टूटी"
                    ]

                    has_problem_word = False

                    for word in problem_words:

                        if word in text_lower:

                            has_problem_word = True
                            break

                    if not has_problem_word:

                        continue

                found.append(category)

                break

    # Catch equivalent complete complaints phrased differently from the
    # hand-written examples, including native Hindi text.
    for category, signals in category_issue_signals.items():
        if category in found:
            continue
        has_subject = any(subject in text_lower for subject in signals["subjects"])
        has_issue = any(issue in text_lower for issue in signals["issues"])
        if has_subject and has_issue:
            found.append(category)

    return found

# 4. CATEGORY PRIORITY


def apply_category_priority(categories, text):

    text_lower = text.lower()

# DRAINAGE PRIORITY

    drainage_indicators = [

        "nali",
        "nali block",
        "nali blocked",
        "nali band",
        "nali overflow",
        "nali ka pani",
        "nali me pani",

        "drain",
        "drainage",
        "wastewater",

        "pani jama",
        "paani jama",
        "water jama",
        "waterlogging",
        "pani bhara",
        "paani bhara",

        "नाली",
        "ड्रेनेज",
        "पानी जमा",
        "पानी भरा",
        "जलभराव"
    ]

    for word in drainage_indicators:

        if word in text_lower:

            return ["Drainage"]

    return categories

# 5. FIND DURATION

def detect_duration(text):

    text_lower = text.lower()

    for pattern in duration_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            return match.group(0)

    return None

# 6. CHECK AMBIGUITY

def check_ambiguity(text, categories):

    

    if len(categories) > 1:

        return True

    return False

# 7. ANALYZE COMPLAINT

def analyze_complaint(text):

    categories = detect_problem(text)

# Apply responsible-department priority
    categories = apply_category_priority(
        categories,
        text
    )

# Detect duration
    duration = detect_duration(text)

# Check ambiguity
    ambiguous = check_ambiguity(
        text,
        categories
    )

# FINAL CATEGORY

    if len(categories) == 1:

        category = categories[0]

    elif len(categories) == 0:

        category = None

    else:

        category = "Ambiguous"

# PROBLEM DETECTED

    problem_detected = (
        len(categories) > 0
    )

    return {

        "problem_detected":
            problem_detected,

        "categories_detected":
            categories,

        "category":
            category,

        "duration":
            duration,

        "ambiguous":
            ambiguous
    }

# 8. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("       COMPLAINT ANALYZER")
    print("===================================")

    complaint = input(
        "\nEnter complaint: "
    )

    result = analyze_complaint(
        complaint
    )

    print("\n===================================")
    print("         ANALYSIS RESULT")
    print("===================================")

    print(
        "\nProblem Detected:",
        result["problem_detected"]
    )

    print(
        "Categories Detected:",
        result["categories_detected"]
    )

    print(
        "Category:",
        result["category"]
    )

    print(
        "Duration:",
        result["duration"]
    )

    print(
        "Ambiguous:",
        result["ambiguous"]
    )

    print("\n===================================")
