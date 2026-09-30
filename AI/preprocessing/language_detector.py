import re


# Common Romanized Hindi words. Avoid words such as "area", "me", and
# "problem": they are also ordinary English words and caused English
# complaints to be mislabeled as Hinglish.
_HINGLISH_WORDS = {
    "aap", "aaya", "aa", "ab", "bahut", "band", "bijli", "chahiye",
    "ganda", "gayi", "gaya", "hai", "hain", "hum", "kab", "kaise",
    "kam", "kar", "ki", "kya", "mera", "meri", "mere", "nahi",
    "nahin", "nali", "paani", "pani", "raha", "rahe", "rahi", "sadak",
    "se", "tha", "thi", "the", "tum", "ya", "yahan",
}


def detect_language(text):
    """Return Hindi, Hinglish, or English based on script and word evidence."""
    if not isinstance(text, str) or not text.strip():
        return "English"

    if any("\u0900" <= char <= "\u097f" for char in text):
        return "Hindi"

    words = re.findall(r"[a-z]+", text.lower())
    matches = sum(word in _HINGLISH_WORDS for word in words)

    # One clear Hindi word is enough (e.g. "pani problem"), while ambiguous
    # single words must not flip a normal English sentence to Hinglish.
    if matches >= 2 or any(word in {"pani", "paani", "bijli", "nahi", "nahin"} for word in words):
        return "Hinglish"

    return "English"
