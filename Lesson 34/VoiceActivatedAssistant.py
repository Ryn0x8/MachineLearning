import speech_recognition as sr
import pyttsx3
from datetime import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print("You said: ", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        return ""
    
def respond_to_command(command):
    if "hello" in command:
        speak("Hello! How can I help you today?")
    elif "your name" in command:
        speak("I am your voice assistant")
    elif "time" in command:
        new = datetime.now().strftime("%H:%M")
        speak(f"The current time is {new}")
    elif "exit" in command:
        speak("Goodbye")
        return False
    else:
        speak("Sorry, I don't understand that command.")
    return True

def main():
    speak("Voice Assistant Activated. Say something.....")
    while True:
        command = get_audio()
        if command and not respond_to_command(command):
            break

if __name__ == "__main__":
    main()