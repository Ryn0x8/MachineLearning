import speech_recognition as sr
import pyttsx3
from googletrans import Translator

def speak(text, language = "en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')

    if language == "en":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak smth in english...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing Speech...")
        text = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    return ""

def translate_text(text, target_language = "es"):
    translator = Translator()
    translation = translator.translate(text, dest = target_language)
    print("Translated Text:", translation.text)
    return translation.text

def display_language_options():
    print("Select target language for translation: ")
    print("1. Spanish (es)")
    print("2. French (fr)")
    print("3. German (de)")
    print("4. Italian (it)")
    print("5. Chinese (zh-cn)")
    print("6. Gujrati (gu)")
    print("7. Hindi (hi)")
    choice = input("Enter the number corresponding to your choice: ")
    language_map = {
        "1": "es",
        "2": "fr",
        "3": "de",
        "4": "it",
        "5": "zh-cn",
        "6": "gu",
        "7": "hi"
    }
    return language_map.get(choice, "es")

def main():
    target_language = display_language_options()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, target_language = target_language)
        speak(translated_text, language = target_language)
        print("Spoken Translated Text.")

if __name__ == "__main__":
    main()