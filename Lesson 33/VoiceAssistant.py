import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3
import json
import datetime
import os
import sys

if not os.path.exists("model"):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    sys.exit(1)

model = Model("model")
recognizer = KaldiRecognizer(model, 16000)
q = queue.Queue()



def speak(text):
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)
    print(f"Assistant: {text}")
    tts_engine.say(text)
    print("Speaking...")
    tts_engine.runAndWait()

speak("Hello! I am your voice assistant. How can I help you today?")

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def process_query(query):
    query = query.lower()
    if "time" in query:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now}"
    elif "date" in query:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {today}"
    elif "hello" in query:
        return "Hello! How can I assist you today?"
    else:
        return "Sorry, I didn't understand that. Please try again."

print("Voice Assistant is listening...")

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels = 1, callback = callback):
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            if text != "":
                print(f"You said: {text}")
                response = process_query(text)
                speak(response)
                
