import tkinter as tk
from tkinter import messagebox
import requests
from config import HF_API

API_URL = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"

headers = {
    "Authorization": f"Bearer {HF_API}"
}

def analyze_sentiment():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text to continue")
        raise

    payload = {"inputs": text}
    try:
        response = requests.post(API_URL, headers = headers, json = payload)
        response.raise_for_status()
        result = response.json()
        # print(result)
        label = result[0][0]["label"]
        score= result[0][0]["score"]
        result_label.config(text=f"Sentiment: {label} (Confidence: {score:.2f})", fg = "green" if label == "POSITIVE" else "red")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Sentiment Analysis")
root.geometry("420x300")
root.resizable(False, False)

tk.Label(root, text = "Enter text for sentiment analysis: ", font = ("Arial", 12)).pack(pady = 10)
text_entry = tk.Text(root, height = 5, width = 50)
text_entry.pack()

analyze_button = tk.Button(
    root, 
    text = "Analyze Sentiment",
    command=analyze_sentiment,
    font = ("Arial", 12),
    bg = "#4CAF50",
    fg = "white"
)

analyze_button.pack(pady = 10)

result_label = tk.Label(root, text = "", font = ("Arial", 12))
result_label.pack(pady = 10)
root.mainloop()
