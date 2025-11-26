import tkinter as tk
from controller import QuizController

def main():
    root = tk.Tk()
    root.title("PyWizz")
    root.geometry("400x600")
    root.resizable(False, False)
    
    app = QuizController(root)
    app.run()
    
    root.mainloop()

if __name__ == "__main__":
    main()