import requests
import sys
from config import HF_API

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
HEADERS = {
    "Authorization": "Bearer " + HF_API
}

LABELS = ["spam", "safe"]

def classify_message(message):
    payload = {
        "inputs": message,
        "parameters": {
            "candidate_labels": LABELS
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"\n❌ API error: {e}")
        return None


def display_result(message, result):
    print("\n📩 Message:")
    print(f"   {message}")

    print("\n🧪 Raw result:", result)

    # 🔒 HARD GUARANTEE: HF returns list → handle list ONLY
    labels = []
    scores = []

    for item in result:
        labels.append(item["label"])
        scores.append(item["score"])

    print("\n📊 Classification:")
    for label, score in zip(labels, scores):
        print(f"   {label.upper():<5} → {score * 100:.2f}%")

    top_label = labels[scores.index(max(scores))]
    verdict = "🚨 SPAM" if top_label == "spam" else "✅ SAFE"

    print(f"\n🧠 Verdict: {verdict}")



def main():
    print("📨 Spam Detection Tool (Improved Model)")
    print("Type 'quit' to exit.\n")

    while True:
        message = input("Enter a message: ").strip()

        if message.lower() == "quit":
            print("\n👋 Goodbye!")
            sys.exit()

        if not message:
            print("⚠️ Please enter a message.")
            continue

        result = classify_message(message)

        if result:
            display_result(message, result)
        else:
            print("⚠️ Could not classify message.")


if __name__ == "__main__":
    main()
