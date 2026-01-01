import requests
import threading
import tkinter as tk
from tkinter import messagebox

URL = "https://uselessfacts.jsph.pl/random.json?language=en"

facts_count = 0
auto_mode = False

def fetch_fact():
    global facts_count
    status_label.config(text = "Fetching Fact")
    try:
        response = requests.get(URL, timeout = 5)
        if response.status_code == 200:
            fact = response.json()["text"]
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, fact)
            status_label.config(text = "Fact Loaded Successfully")
            facts_count += 1
            counter_label.config(text = "Facts Viewed: " + str(facts_count))

        else:
            status_label.config(text  = "Failed to fetch the Fact")
        
    except:
        status_label.config(text  = "Error occurred while fetching the Fact")

def get_fact():
    threading.Thread(target = fetch_fact, daemon = True).start()

def copy_fact():
    root.clipboard_clear()
    root.clipboard_append(text_area.get(1.0, tk.END))
    status_label.config(text = "Fact copied to clipboard")

def toggle_auto():
    global auto_mode
    auto_mode = not auto_mode
    if auto_mode:
        auto_button.config(text = "Auto Mode: ON")
        auto_fetch()
    else:
        auto_button.config(text = "Auto Mode: OFF")
        status_label.config(text = "Auto Mode Stopped")

def auto_fetch():
    if auto_mode:
        get_fact()
        root.after(5000, auto_fetch)

root = tk.Tk()
root.title("Interactive Facts Viewer")
root.geometry("550x380")
root.resizable(False, False)
root.config(bg = "#121212")

tk.Label(
    root,
    text = "Technology Facts Hub",
    font = ("Helvetica", 20, "bold"),
    bg = "#121212",
    fg = "#00FF00"
).pack(pady = 10)

text_area = tk.Text(
    root,
    width = 60,
    height = 8,
    wrap = tk.WORD,
    font = ("Helvetica", 12),
    bg = "#1E1E1E",
    fg = "#FFFFFF",
    insertbackground="white"
)

text_area.pack(pady = 10)


btn_frame = tk.Frame(root, bg = "#121212")
btn_frame.pack(pady = 10)

tk.Button(
    btn_frame,
    text = "Fetch Fact",
    command= get_fact,
    bg = "#007ACC",
    fg = "#FFFFFF",
    font = ("Helvetica", 12, "bold"),
    width = 12
).grid(row = 0, column = 0, padx = 10)


tk.Button(
    btn_frame,
    text = "Copy Fact",
    command= copy_fact,
    bg = "#007ACC",
    fg = "#FFFFFF",
    font = ("Helvetica", 12),
    width = 12
).grid(row = 0, column = 1, padx = 10)

auto_button =tk.Button(
    btn_frame,
    text = "Auto Mode",
    command= toggle_auto,
    bg = "#BCDBF1",
    fg = "#000000",
    font = ("Helvetica", 12, "bold"),
    width = 12
)

auto_button.grid(row = 0, column = 2, padx = 10)

counter_label = tk.Label(
    root, text = "Facts Viewed: 0", font = ("Helvetica", 12), bg = "#121212", fg = "#00FF00"
)
counter_label.pack(pady = 5)

status_label = tk.Label(
    root, text = "Welcome to Technology Facts Hub", font = ("Helvetica", 10), bg = "#121212", fg = "#00FF00", anchor = "w"
)

status_label.pack(fill = tk.X, side = tk.BOTTOM)

root.mainloop()