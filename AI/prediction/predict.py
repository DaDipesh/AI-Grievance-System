import joblib
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AI_DIR = Path(__file__).resolve().parents[1]

# 1. LOAD TRAINED MODEL

model = joblib.load(AI_DIR / "models" / "trained_model.pkl")
vectorizer = joblib.load(AI_DIR / "models" / "vectorizer.pkl")

# 2. TAKE COMPLAINT

complaint = input("\nEnter your complaint: ")

# 3. CONVERT TEXT INTO TF-IDF

complaint_vector = vectorizer.transform([complaint])

# 4. PREDICT CATEGORY

prediction = model.predict(complaint_vector)

# 5. GET PROBABILITIES

probabilities = model.predict_proba(complaint_vector)[0]

categories = model.classes_

# 6. FIND CONFIDENCE

confidence = max(probabilities) * 100

# 7. DISPLAY RESULT

print("\n===================================")
print("        AI GRIEVANCE RESULT")
print("===================================")

print("\nComplaint:")
print(complaint)

print("\nPredicted Category:")
print(prediction[0])

print("\nConfidence:")
print(round(confidence, 2), "%")

# 8. SHOW ALL CATEGORY PROBABILITIES

print("\nCategory Probabilities:")

for category, probability in zip(categories, probabilities):

    print(
        category,
        ":",
        round(probability * 100, 2),
        "%"
    )

# 9. CONFIDENCE CHECK

print("\n===================================")

if confidence >= 70:

    print("✅ AI prediction accepted")

elif confidence >= 50:

    print("⚠️ AI is uncertain - clarification recommended")

else:

    print("❌ Low confidence - Human Review required")

print("===================================")
