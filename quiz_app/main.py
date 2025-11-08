# main.py
import tkinter as tk
from controller import QuizController

def main():
    root = tk.Tk()
    app = QuizController(root)
    root.mainloop()

if __name__ == "__main__":
    main()