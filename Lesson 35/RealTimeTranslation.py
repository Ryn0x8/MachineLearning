import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import pyttsx3
from googletrans import Translator
from datetime import datetime
import threading
import speech_recognition as sr

recognizer = sr.Recognizer()
translator = Translator()

running = False

languages = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Japanese": "ja",
}

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.say(text)
    engine.runAndWait()

def listen(lang_code):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language=lang_code)
        except:
            return None

def conversation():
    global running
    running =  True
    selected_lang = language_var.get()
    target_lang_code = languages[selected_lang]
    chat_area.insert(tk.END, f"Conversation started in {selected_lang}...\n")
    chat_area.see(tk.END)
    while running:
        chat_area.insert(tk.END, "Person 1 (English): Listening...\n")
        chat_area.see(tk.END)
        text = listen("en-US")
        if text:
            chat_area.insert(tk.END, f"Person 1: {text}\n")
            translated = translator.translate(text, dest=target_lang_code).text
            chat_area.insert(tk.END, f"{selected_lang}: {translated}\n")
            chat_area.see(tk.END)
            speak(translated)
            if text.lower() in ["stop", "exit", "quit"]:
                running = False
                chat_area.insert(tk.END, "Conversation ended.\n")
                chat_area.see(tk.END)

        if not running:
            break

        chat_area.insert(tk.END, f"Person 2 ({selected_lang}): Listening...\n")
        chat_area.see(tk.END)
        text_other = listen(target_lang_code)
        if text_other:
            chat_area.insert(tk.END, f"Person 2: {text_other}\n")
            translated_back = translator.translate(text_other, dest="en").text
            chat_area.insert(tk.END, f"English: {translated_back}\n")
            chat_area.see(tk.END)
            speak(translated_back)
            if text_other.lower() in ["stop", "exit", "quit"]:
                running = False
                chat_area.insert(tk.END, "Conversation ended.\n")
                chat_area.see(tk.END)
                break
        chat_area.insert(tk.END, "---------Conversation Ended------------\n")
        chat_area.see(tk.END)

def start_conversation():
    thread = threading.Thread(target=conversation)
    thread.start()

def stop_conversation():
    global running
    running = False

def save_conversation():
    content = chat_area.get("1.0", tk.END)
    if not content.strip():
        messagebox.showwarning("No Conversation", "There is no conversation to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    if file_path:
        with open(file_path, "w", encoding = "utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Conversation saved to {file_path}")

root = tk.Tk()
root.title("Real-Time Translation Conversation")
root.geometry("650x600")

language_var = tk.StringVar(value="Spanish")
language_menu = tk.OptionMenu(root, language_var, *languages.keys())
language_menu.pack(pady=5)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font = ("Arial", 12))
chat_area.pack(padx = 10, pady = 10, fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(pady = 5)

start_button = tk.Button(button_frame, text = "Start", command = start_conversation, bg = "green", fg = "white", width = 10)
start_button.grid(row = 0, column = 0, padx = 5)

stop_button = tk.Button(button_frame, text = "Stop", command = stop_conversation, bg = "red", fg = "white", width = 10)
stop_button.grid(row = 0, column = 1, padx = 5 ) 

save_button = tk.Button(button_frame, text = "Save", command = save_conversation, bg = "blue", fg = "white", width = 10)
save_button.grid(row = 0, column = 2, padx = 5 ) 

root.mainloop()

        