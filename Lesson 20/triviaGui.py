import requests
import tkinter as tk
from tkinter import messagebox
import html
import random

BASE_URL = "https://opentdb.com/api.php?amount=10&type=multiple"

LEVELS = {
    "Easy": ("easy", 20),
    "Medium": ("medium", 15),
    "Hard": ("hard", 10)
}

BG_COLOR = "#FFEBB8"
BUTTON_COLOR = "#375362"
BUTTON_TEXT_COLOR = "#FFFFFF"
TIMER_COLOR = "#FF5733"
QUESTION_COLOR = "#333333"

class TriviaQuiz:
    def __init__(self, root):
        self.root  = root
        self.root.title("Trivia Quiz")
        self.root.geometry("650x450")
        self.root.config(bg = BG_COLOR)
        
        self.score = 0
        self.q_index = 0
        self.time_left = 0
        self.questions = []
        self.timer_id = None
        self.timer_label = None

        self.create_level_screen()

    def create_level_screen(self):
        self.clear_screen()

        tk.Label(self.root, text = "Trivia Quiz", font = ("Arial", 24, "bold"), bg = BG_COLOR, fg=QUESTION_COLOR).pack(pady = 20)
        tk.Label(self.root, text = "Select the Difficulty Level: ", font = ("Arial", 16, "bold"), bg = BG_COLOR, fg=QUESTION_COLOR).pack(pady = 10)


        for level in LEVELS:
            tk.Button(self.root, 
                      text = level, 
                      width = 20,
                      activebackground="#274156",
                      command = lambda l=level: self.start_quiz(l), 
                      bg = BUTTON_COLOR, 
                      fg = BUTTON_TEXT_COLOR, 
                      font = ("Arial", 12, "bold")
                      ).pack(pady = 5)
            
    def start_quiz(self, level):
        self.difficulty, self.time_limit = LEVELS[level]
        self.questions = self.get_questions(self.difficulty)
        if not self.questions:
            messagebox.showerror("Error", "Failed to fetch questions. Try agan")
            return
        
        self.score = 0
        self.q_index = 0
        self.show_questions()

    def get_questions(self, difficulty):
        try:
            response = requests.get(f"{BASE_URL}&difficulty={difficulty}", timeout = 10)
            if response.status_code == 200:
                data = response.json()
                if data["response_code"]== 0:
                    return data["results"]
        except:
            return None
        
    def show_questions(self):
        self.clear_screen()
        self.time_left = self.time_limit

        q = self.questions[self.q_index]
        self.correct_answer = html.unescape(q["correct_answer"])
        options = [html.unescape(a) for a in q["incorrect_answers"]]
        options.append(self.correct_answer)
        random.shuffle(options)

        tk.Label(self.root, text = f"Question No: {self.q_index + 1}", font = ("Arial", 14, "bold"), bg = BG_COLOR).pack(pady = 5)
        tk.Label(self.root, text = html.unescape(q["question"]), wraplength=600, font = ("Arial", 14, "bold"), bg = BG_COLOR, fg=QUESTION_COLOR).pack(pady = 15)

        self.timer_label = tk.Label(self.root, text = f"Time Left: {self.time_left} sec", font = ("Arial", 12, "bold"), bg = BG_COLOR, fg = TIMER_COLOR)
        self.timer_label.pack(pady = 5)
        for option in options:
            tk.Button(self.root,
                      text = option,
                      width = 30,
                      activebackground="#274156",
                      wraplength = 550,
                      command = lambda o=option: self.check_answer(o),
                      bg = BUTTON_COLOR,
                      fg = BUTTON_TEXT_COLOR,
                      font = ("Arial", 12, "bold"),
                      relief = "raised",
                      bd = 2

                      ).pack(pady = 6, padx = 20, fill = "x")
            
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text = f"Time Left: {self.time_left} sec")
        if self.time_left > 0:
            self.time_left -=1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self.next_question()

    def check_answer(self, selected_option):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if selected_option == self.correct_answer:
            self.score +=1
            messagebox.showinfo("Correct!", "You selected the correct answer!")
        else:
            messagebox.showinfo("Incorrect!", f"The correct answer was: {self.correct_answer}")

        self.next_question()

    def next_question(self):
        self.q_index +=1
        if self.q_index < len(self.questions):
            self.show_questions()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()
        tk.Label(self.root, text = "Quiz Completed!", font = ("Arial", 24, "bold"), bg = BG_COLOR, fg= QUESTION_COLOR).pack(pady = 20)
        tk.Label(self.root, text = f"Your Score: {self.score}/{len(self.questions)}", font  = ("Arial", 18, "bold"), bg = BG_COLOR).pack(pady = 10)
        tk.Button(self.root, text = "Play Again!", width = 20, font = ("Arial", 12, "bold"), bg = BUTTON_COLOR, fg = BUTTON_TEXT_COLOR, command = self.create_level_screen).pack(pady = 7)
        tk.Button(self.root, text = "Exit", width = 20, font = ("Arial", 12), bg = BUTTON_COLOR, fg = BUTTON_TEXT_COLOR, command = self.root.quit).pack(pady = 5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    quiz = TriviaQuiz(root)
    root.mainloop()