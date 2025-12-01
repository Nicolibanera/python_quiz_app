# this is for the result

import tkinter as tk

class ResultView(tk.Frame):
    def __init__(self, root, controller):
        super().__init__(root, bg="white")
        self.controller = controller

        self.title_label = tk.Label(self, text="Quiz Result", font=("Arial", 22, "bold"), bg="white")
        self.title_label.pack(pady=20)

        self.score_label = tk.Label(self, text="", font=("Arial", 18), bg="white")
        self.score_label.pack(pady=10)

        self.percent_label = tk.Label(self, text="", font=("Arial", 16), bg="white")
        self.percent_label.pack(pady=10)

        self.level_label = tk.Label(self, text="", font=("Arial", 16), bg="white")
        self.level_label.pack(pady=10)

        self.home_btn = tk.Button(self, text="Back to Home", command=self.controller.show_page1)
        self.home_btn.pack(pady=20)

    def update_result(self, score, total):
        percent = round((score / total) * 100)

        # to set score of what and how you performed
        self.score_label.config(text=f"Score: {score}/{total}")
        self.percent_label.config(text=f"Percentage: {percent}%")
        self.level_label.config(text=self.get_level(percent))
        

        #to show remarks on how you did
    def get_level(self, percent):
        if percent == 100:
            return "Level: Perfect"
        elif percent >= 70:
            return "Level: Great"
        elif percent >= 40:
            return "Level:  Keep Improving"
        else:
            return "Level: Try Again"
